import pytest

from django.contrib.gis.geos import Point
from unittest import mock

from erp import schema
from erp import forms
from erp.models import Commune, Erp
from erp.provider import geocoder

from tests.fixtures import data

POINT = Point((0, 0))


@pytest.fixture
def paris_commune():
    c = Commune(nom="Paris", departement="75", code_insee="75111", geom=POINT)
    c.save()


@pytest.fixture
def form_data(data):
    return {
        "source": "sirene",
        "source_id": "xxx",
        "user": data.niko,
        "user_type": "public",
        "nom": "plop",
        "numero": "4",
        "voie": "rue de la paix",
        "lieu_dit": "blah",
        "code_postal": "75002",
        "commune": "Paris",
    }


@pytest.fixture
def geocoder_result_ok():
    return {
        "geom": POINT,
        "numero": "4",
        "voie": "Rue de la Paix",
        "lieu_dit": None,
        "code_postal": "75002",
        "commune": "Paris",
        "code_insee": "75111",
    }


@pytest.mark.django_db
def test_CustomRegistrationForm():
    form = forms.CustomRegistrationForm()
    assert form.is_valid() is False

    form = forms.CustomRegistrationForm({"username": "toto@toto.com"})
    assert form.is_valid() is False
    assert forms.USERNAME_RULES in form.errors["username"]

    form = forms.CustomRegistrationForm({"username": "toto+toto"})
    assert form.is_valid() is False
    assert forms.USERNAME_RULES in form.errors["username"]

    form = forms.CustomRegistrationForm(
        {"username": "".join(map(lambda _: "x", range(0, 33)))}
    )  # 33c length string
    assert form.is_valid() is False
    assert (
        "Assurez-vous que cette valeur comporte au plus 32 caractères (actuellement 33)."
        in form.errors["username"]
    )

    form = forms.CustomRegistrationForm({"username": "jean-pierre.timbault_42"})
    assert "username" not in form.errors


def test_AdminAccessibiliteForm_sanitaires_adaptes_value_mapping(data):
    data.accessibilite.sanitaires_adaptes = 12
    data.accessibilite.save()

    form = forms.AdminAccessibiliteForm(instance=data.accessibilite)

    assert form.initial["sanitaires_adaptes"] == 1


@pytest.mark.django_db
def test_BaseErpForm_get_adresse_query(
    form_data, mocker, geocoder_result_ok, paris_commune
):
    mocker.patch("erp.provider.geocoder.geocode", return_value=geocoder_result_ok)
    form = forms.AdminErpForm(form_data)
    form.is_valid()  # populates cleaned_data
    assert form.get_adresse_query() == "4 Rue de la Paix, Paris"


@pytest.mark.django_db
def test_BaseErpForm_geocode_adresse(
    form_data, mocker, geocoder_result_ok, paris_commune
):
    mocker.patch("erp.provider.geocoder.geocode", return_value=geocoder_result_ok)
    form = forms.AdminErpForm(form_data)
    form.is_valid()
    assert form.cleaned_data["geom"] == POINT
    assert form.cleaned_data["numero"] == "4"
    assert form.cleaned_data["voie"] == "Rue de la Paix"
    assert form.cleaned_data["lieu_dit"] is None
    assert form.cleaned_data["code_postal"] == "75002"
    assert form.cleaned_data["commune"] == "Paris"
    assert form.cleaned_data["code_insee"] == "75111"


@pytest.mark.django_db
def test_BaseErpForm_clean_geom_missing(data, mocker):
    mocker.patch(
        "erp.provider.geocoder.geocode",
        return_value={
            "geom": None,
            "numero": None,
            "voie": "Grand rue",
            "lieu_dit": None,
            "code_postal": "34830",
            "commune": "Jacou",
            "code_insee": "34120",
        },
    )
    form = forms.PublicErpEditInfosForm(
        {
            "source": "sirene",
            "source_id": "xxx",
            "user": data.niko,
            "user_type": "public",
            "activite": str(data.boulangerie.pk),
            "recevant_du_public": "on",
            "nom": "test erp",
            "numero": "4",
            "voie": "Grand rue",
            "lieu_dit": "",
            "code_postal": "34830",
            "commune": "Jacou",
        }
    )
    assert form.is_valid() is False
    assert "voie" in form.errors
    assert "Adresse non localisable" in form.errors["voie"][0]


@pytest.mark.django_db
def test_BaseErpForm_clean_code_postal_mismatch(data, mocker):
    mocker.patch(
        "erp.provider.geocoder.geocode",
        return_value={
            "geom": POINT,
            "numero": None,
            "voie": "Grand rue",
            "lieu_dit": None,
            "code_postal": "34830",
            "commune": "Jacou",
            "code_insee": "34120",
        },
    )
    form = forms.PublicErpEditInfosForm(
        {
            "source": "sirene",
            "source_id": "xxx",
            "user": data.niko,
            "user_type": "public",
            "activite": str(data.boulangerie.pk),
            "recevant_du_public": "on",
            "nom": "plop",
            "numero": "4",
            "voie": "rue de la paix",
            "lieu_dit": "",
            "code_postal": "75002",
            "commune": "Paris",
        }
    )
    assert form.is_valid() is False
    assert "code_postal" in form.errors
    assert "pas localisable au code postal 75002" in form.errors["code_postal"][0]


@pytest.mark.django_db
def test_BaseErpForm_clean_numero_mismatch(data, mocker):
    mocker.patch(
        "erp.provider.geocoder.geocode",
        return_value={
            "geom": POINT,
            "numero": None,
            "voie": "Grand rue",
            "lieu_dit": None,
            "code_postal": "34830",
            "commune": "Jacou",
            "code_insee": "12345",
        },
    )
    form = forms.PublicErpEditInfosForm(
        {
            "source": "sirene",
            "source_id": "xxx",
            "user": data.niko,
            "user_type": "public",
            "activite": str(data.boulangerie.pk),
            "recevant_du_public": "on",
            "nom": "test erp",
            "numero": "4",
            "voie": "Grand rue",
            "lieu_dit": "",
            "code_postal": "34830",
            "commune": "Jacou",
        }
    )
    assert form.is_valid() is True
    assert "numero" not in form.errors
    assert form.cleaned_data["numero"] == "4"
    form.save()
    Erp.objects.get(slug="test-erp").numero == "4"


def test_BaseErpForm_invalid_on_empty_geocode_results(form_data, mocker):
    mocker.patch("erp.provider.geocoder.geocode", return_value=None)
    form = forms.AdminErpForm(form_data)
    assert form.is_valid() is False


@pytest.mark.django_db
def test_BaseErpForm_valid_on_geocoded_results(
    form_data, mocker, geocoder_result_ok, paris_commune
):
    mocker.patch("erp.provider.geocoder.geocode", return_value=geocoder_result_ok)
    form = forms.AdminErpForm(form_data)
    assert form.is_valid() is True


def test_BaseErpForm_retrieve_code_insee_from_manual_input(
    data, mocker, geocoder_result_ok
):
    mocker.patch(
        "erp.provider.geocoder.geocode",
        return_value={
            "geom": POINT,
            "numero": "12",
            "voie": "Grand Rue",
            "lieu_dit": None,
            "code_postal": "34830",
            "commune": "Jacou",
            "code_insee": "34120",
        },
    )
    geocode = mocker.spy(geocoder, "geocode")
    form = forms.PublicErpAdminInfosForm(
        {
            "source": Erp.SOURCE_PUBLIC,
            "source_id": "",
            "geom": None,
            "nom": "xxx jacou",
            "activite": data.boulangerie.pk,
            "numero": "12",
            "voie": "grand rue",
            "lieu_dit": "",
            "code_postal": "34830",
            "commune": "jacou",
            "siret": "",
            "contact_email": "",
            "site_internet": "",
            "telephone": "",
            "recevant_du_public": "on",
        }
    )
    assert form.is_valid() is True
    geocode.assert_called_with("12 grand rue, jacou", citycode="34120")


# ProviderGlobalSearchForm


def test_ProviderGlobalSearchForm(data):
    form = forms.ProviderGlobalSearchForm(initial={"code_insee": data.jacou.code_insee})

    assert form.initial["commune_search"] == "Jacou (34 - Hérault)"


# ViewAccessibiliteForm


def test_ViewAccessibiliteForm_empty():
    form = forms.ViewAccessibiliteForm()
    data = form.get_accessibilite_data()
    assert list(data.keys()) == []


def test_ViewAccessibiliteForm_filled():
    form = forms.ViewAccessibiliteForm(
        {
            "entree_reperage": True,
            "transport_station_presence": True,
            "stationnement_presence": True,
            "cheminement_ext_presence": True,
            "accueil_visibilite": True,
            "sanitaires_presence": True,
            "commentaire": "plop",
        }
    )
    data = form.get_accessibilite_data()
    assert list(data.keys()) == [
        "Transports en commun",
        "Stationnement",
        "Cheminement extérieur",
        "Entrée",
        "Accueil",
        "Sanitaires",
        "Commentaire",
    ]


def test_ViewAccessibiliteForm_filled_null_comment():
    form = forms.ViewAccessibiliteForm(
        {
            "sanitaires_presence": True,
            "commentaire": "",
        }
    )
    data = form.get_accessibilite_data()
    assert list(data.keys()) == ["Sanitaires"]


def test_ViewAccessibiliteForm_serialized():
    form = forms.ViewAccessibiliteForm(
        {
            "entree_reperage": True,
        }
    )
    data = form.get_accessibilite_data()
    field = data["Entrée"]["fields"][0]

    assert field["template_name"] == "django/forms/widgets/select.html"
    assert field["name"] == "entree_reperage"
    assert field["label"] == schema.get_label("entree_reperage")
    assert field["help_text_ui"] == schema.get_help_text_ui("entree_reperage")
    assert field["value"] is True
    assert field["warning"] is False
