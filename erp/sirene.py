import base64
import json

from api_insee import ApiInsee
from api_insee.criteria import Field
from django.conf import settings
from stdnum.fr import siret
from stdnum import exceptions as stdnum_ex
from urllib.parse import quote_plus
from urllib.error import HTTPError

CODE_INSEE = "codeCommuneEtablissement"
CODE_POSTAL = "codePostalEtablissement"
COMMUNE = "libelleCommuneEtablissement"
COMPLEMENT = "complementAdresseEtablissement"
INDICE = "indiceRepetitionEtablissement"
NOM = "denominationUniteLegale"
NUMERO = "numeroVoieEtablissement"
STATUT = "etatAdministratifUniteLegale"
SIRET = "siret"
TYPE_VOIE = "typeVoieEtablissement"
VOIE = "libelleVoieEtablissement"

SIRET_API_REQUEST_FIELDS = [
    STATUT,
    NOM,
    SIRET,
    COMPLEMENT,
    NUMERO,
    INDICE,
    TYPE_VOIE,
    VOIE,
    CODE_POSTAL,
    COMMUNE,
    CODE_INSEE,
]


def get_client():
    return ApiInsee(
        key=settings.INSEE_API_CLIENT_KEY, secret=settings.INSEE_API_SECRET_KEY,
    )


def base64_decode_etablissement(data):
    try:
        return json.loads(base64.urlsafe_b64decode(data).decode())
    except Exception:
        raise RuntimeError("Impossible de décoder les informations de l'établissement")


def base64_encode_etablissement(etablissement):
    try:
        return base64.urlsafe_b64encode(json.dumps(etablissement).encode()).decode(
            "utf-8"
        )
    except Exception:
        raise RuntimeError("Impossible d'encoder les informations de l'établissement")


def format_siret(value):
    return siret.format(value, separator="")


def parse_etablissement(etablissement):
    # To the reader: I'm so sorry.
    assert "uniteLegale" in etablissement
    uniteLegale = etablissement["uniteLegale"]
    assert SIRET in etablissement
    siret = etablissement.get(SIRET)
    assert "adresseEtablissement" in etablissement
    adresseEtablissement = etablissement["adresseEtablissement"]
    numeroVoieEtablissement = adresseEtablissement.get(NUMERO)
    indiceRepetitionEtablissement = adresseEtablissement.get(INDICE)
    typeVoieEtablissement = adresseEtablissement.get(TYPE_VOIE)
    libelleVoieEtablissement = adresseEtablissement.get(VOIE)
    return dict(
        actif=uniteLegale[STATUT] == "A",
        nom=uniteLegale[NOM],
        siret=siret,
        numero=" ".join(
            [numeroVoieEtablissement or "", indiceRepetitionEtablissement or "",]
        ).strip()
        or None,
        voie=" ".join(
            [typeVoieEtablissement or "", libelleVoieEtablissement or "",]
        ).strip()
        or None,
        lieu_dit=adresseEtablissement.get(COMPLEMENT),
        code_postal=adresseEtablissement.get(CODE_POSTAL),
        commune=adresseEtablissement.get(COMMUNE),
        code_insee=adresseEtablissement.get(CODE_INSEE),
    )


def find_etablissements(nom, code_postal=None, limit=5):
    q = Field(NOM, f"{quote_plus(nom)}~")
    if code_postal is not None:
        q = q & Field(CODE_POSTAL, code_postal)
    try:
        response = (
            get_client().siret(q=q, nombre=limit, masquerValeursNulles=True,).get()
        )
    except HTTPError as err:
        if err.code == 404:
            raise RuntimeError("Aucun résultat")
        else:
            raise RuntimeError("Le service INSEE est indisponible.")
    assert "etablissements" in response
    results = []
    for etablissement in response["etablissements"]:
        results.append(parse_etablissement(etablissement))
    return results


def get_siret_info(value):
    try:
        response = get_client().siret(value, champs=SIRET_API_REQUEST_FIELDS,).get()
    except HTTPError:
        raise RuntimeError("Le service INSEE est indisponible")
    assert "etablissement" in response
    return parse_etablissement(response["etablissement"])


def validate_siret(value):
    try:
        return siret.validate(value)
    except stdnum_ex.ValidationError:
        return None
