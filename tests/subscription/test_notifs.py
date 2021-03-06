import pytest
from django.conf import settings

from django.contrib.gis.geos import Point
from django.core import mail
from django.test import Client
from django.urls import reverse

from erp.models import Accessibilite, Erp
from subscription.models import ErpSubscription
from subscription.jobs import notify_changed_erps

from tests.fixtures import data

from reversion.models import Version


@pytest.fixture
def client():
    return Client()


def niko_create_erp_and_subscribe_updates(client, data, mocker):
    "TODO: make this a reusable test helper"
    # setup geocoder mock
    mocker.patch(
        "erp.provider.geocoder.geocode",
        return_value={
            "geom": Point((0, 0)),
            "numero": "4",
            "voie": "Grand rue",
            "lieu_dit": "",
            "code_postal": "34830",
            "commune": "Jacou",
            "code_insee": "34120",
        },
    )
    # auth user
    client.login(username="niko", password="Abc12345!")
    # create erp admin data
    response = client.post(
        reverse("contrib_admin_infos"),
        data={
            "source": "sirene",
            "source_id": "xxx",
            "nom": "niko erp",
            "recevant_du_public": True,
            "activite": data.boulangerie.pk,
            "siret": "21690266800013",
            "numero": "4",
            "voie": "Grand rue",
            "lieu_dit": "",
            "code_postal": "34830",
            "commune": "JACOU",
            "site_internet": "http://google.com/",
        },
        follow=True,
    )
    assert response.status_code == 200
    assert response.context["form"].errors == {}
    erp = Erp.objects.get(nom="niko erp")
    # add some a11y data
    response = client.post(
        reverse("contrib_sanitaires", kwargs={"erp_slug": erp.slug}),
        data={
            "sanitaires_presence": "True",
            "sanitaires_adaptes": "1",
        },
        follow=True,
    )
    assert response.status_code == 200
    assert response.context["form"].errors == {}
    erp = Erp.objects.get(nom="niko erp")
    # publish erp
    response = client.post(
        reverse("contrib_publication", kwargs={"erp_slug": erp.slug}),
        data={
            "user_type": Erp.USER_ROLE_PUBLIC,
            "published": "on",
            "certif": "on",
        },
        follow=True,
    )
    assert response.status_code == 200
    # ensure erp is published
    erp = Erp.objects.get(nom="niko erp")
    assert erp.is_online() is True
    # subscribe user
    ErpSubscription.subscribe(erp, data.niko)
    return erp


def test_notification_erp(client, data, mocker):
    erp = niko_create_erp_and_subscribe_updates(client, data, mocker)

    # sophie updates this erp data
    client.login(username="sophie", password="Abc12345!")
    response = client.post(
        reverse("contrib_edit_infos", kwargs={"erp_slug": erp.slug}),
        data={
            "source": "sirene",
            "source_id": "xxx",
            "nom": "sophie erp",
            "recevant_du_public": True,
            "activite": data.boulangerie.pk,
            "siret": "21690266800013",
            "numero": "4",
            "voie": "Grand rue",
            "lieu_dit": "",
            "code_postal": "34830",
            "commune": "Jacou",
            "site_internet": "http://google.com/",
            "action": "contribute",
        },
        follow=True,
    )

    assert response.status_code == 200
    updated_erp = Erp.objects.get(slug=erp.slug)
    assert response.context["form"].errors == {}
    assert updated_erp.nom == "sophie erp"
    assert Version.objects.count() != 0

    notify_changed_erps.job()
    unsubscribe_url = reverse("unsubscribe_erp", kwargs={"erp_slug": erp.slug})

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [data.niko.email]
    assert "Vous avez reçu de nouvelles contributions" in mail.outbox[0].subject
    assert "sophie erp" in mail.outbox[0].body
    assert "34830 Jacou" in mail.outbox[0].body
    assert "sophie a mis à jour les informations suivantes" in mail.outbox[0].body
    assert 'nom: "niko erp" devient "sophie erp"' in mail.outbox[0].body
    assert f'{settings.SITE_ROOT_URL}{unsubscribe_url}' in mail.outbox[0].body
    assert updated_erp.get_absolute_url() in mail.outbox[0].body


def test_notification_accessibilite(client, data, mocker):
    erp = niko_create_erp_and_subscribe_updates(client, data, mocker)

    # sophie updates this erp accessibilite data
    client.login(username="sophie", password="Abc12345!")

    response = client.post(
        reverse("contrib_sanitaires", kwargs={"erp_slug": erp.slug}),
        data={
            "sanitaires_presence": "False",
            "sanitaires_adaptes": "0",
            "action": "contribute",
        },
        follow=True,
    )

    assert response.status_code == 200
    updated_acc = Accessibilite.objects.get(erp__slug=erp.slug)
    assert Version.objects.count() != 0

    notify_changed_erps.job()

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [data.niko.email]
    assert "Vous avez reçu de nouvelles contributions" in mail.outbox[0].subject
    assert "niko erp" in mail.outbox[0].body
    assert "34830 Jacou" in mail.outbox[0].body
    assert "sophie a mis à jour les informations suivantes" in mail.outbox[0].body
    assert 'Sanitaires: "True" devient "False"' in mail.outbox[0].body
    assert 'Sanitaires adaptés: "1" devient "0"' in mail.outbox[0].body
    assert updated_acc.erp.get_absolute_url() in mail.outbox[0].body


def test_notification_skip_owner(client, data):
    client.login(username="niko", password="Abc12345!")
    response = client.post(
        reverse("contrib_edit_infos", kwargs={"erp_slug": data.erp.slug}),
        data={
            "source": "sirene",
            "source_id": "xxx",
            "nom": "Test update",
            "recevant_du_public": True,
            "activite": data.boulangerie.pk,
            "siret": "21690266800013",
            "numero": "12",
            "voie": "GRAND RUE",
            "lieu_dit": "",
            "code_postal": "34830",
            "commune": "JACOU",
            "site_internet": "http://google.com/",
            "action": "contribute",
        },
        follow=True,
    )

    assert response.status_code == 200

    # niko is owner and shouldn't be notified
    notify_changed_erps.job()

    assert len(mail.outbox) == 0


def test_erp_publication_subscription_option(data, client):
    client.login(username="niko", password="Abc12345!")

    # user subscribes to updates
    response = client.post(
        reverse("contrib_publication", kwargs={"erp_slug": data.erp.slug}),
        data={
            "user_type": Erp.USER_ROLE_PUBLIC,
            "published": "on",
            "certif": "on",
            "subscribe": "on",
        },
        follow=True,
    )
    assert response.status_code == 200
    assert ErpSubscription.objects.filter(erp=data.erp, user=data.niko).count() == 1

    # user unsubscribes from updates
    response = client.post(
        reverse("contrib_publication", kwargs={"erp_slug": data.erp.slug}),
        data={
            "user_type": Erp.USER_ROLE_PUBLIC,
            "published": "on",
            "certif": "on",
            "subscribe": "on",
        },
        follow=True,
    )
    assert response.status_code == 200
    assert ErpSubscription.objects.filter(erp=data.erp, user=data.niko).count() == 1
