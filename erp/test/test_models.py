import pytest

from django.core.exceptions import ValidationError

from ..models import Erp

from .fixtures import data


def test_Erp_clean_validates_code_postal(data, capsys):
    erp = Erp.objects.create(nom="x", code_postal="1234")
    with pytest.raises(ValidationError) as excinfo:
        erp.clean()
    assert "code_postal" in excinfo.value.error_dict


def test_Erp_clean_validates_voie(data, capsys):
    erp = Erp.objects.create(nom="x", code_postal="12345")
    with pytest.raises(ValidationError) as excinfo:
        erp.clean()
    assert "voie" in excinfo.value.error_dict
    assert "lieu_dit" in excinfo.value.error_dict


def test_Erp_clean_handles_commune_ext(data, capsys):
    erp = Erp.objects.create(nom="x", code_postal="12345", voie="y", commune="missing")
    with pytest.raises(ValidationError) as excinfo:
        erp.clean()
    assert "commune" in excinfo.value.error_dict

    erp = Erp.objects.create(nom="x", code_postal="34830", voie="y", commune="jacou")
    erp.clean()
    assert erp.commune_ext == data.jacou


def test_Erp_editable_by(data):
    assert data.erp.editable_by(data.niko) == True
    assert data.erp.editable_by(data.sophie) == False