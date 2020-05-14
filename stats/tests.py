import pytest

from django.test import Client
from django.urls import reverse

from erp.models import Commune, Erp


@pytest.mark.django_db
def test_home():
    c = Client()
    response = c.get(reverse("stats_home"))
    assert response.status_code == 200
