import json
import logging

from api_insee import ApiInsee
from api_insee import criteria
from api_insee.exeptions.request_exeption import RequestExeption
from django.conf import settings
from stdnum.fr import siret
from stdnum import exceptions as stdnum_ex
from urllib.error import HTTPError

from erp.provider.voies import TYPES_VOIE


ACTIVITE_NAF = "activitePrincipaleUniteLegale"
CODE_INSEE = "codeCommuneEtablissement"
CODE_POSTAL = "codePostalEtablissement"
COMMUNE = "libelleCommuneEtablissement"
COMPLEMENT = "complementAdresseEtablissement"
DATE_DEBUT = "dateDebut"
ETAT_ETABLISSEMENT = "etatAdministratifEtablissement"
INDICE = "indiceRepetitionEtablissement"
NUMERO = "numeroVoieEtablissement"
NOM_ENSEIGNE1 = "enseigne1Etablissement"
NOM_ENSEIGNE2 = "denominationUsuelleEtablissement"
NOM_ENSEIGNE3 = "denominationUsuelle1UniteLegale"
PERIODES_ETABLISSEMENT = "periodesEtablissement"
PERSONNE_NOM = "nomUniteLegale"
PERSONNE_PRENOM = "prenomUsuelUniteLegale"
RAISON_SOCIALE = "denominationUniteLegale"
STATUT = "etatAdministratifUniteLegale"
SIRET = "siret"
TYPE_VOIE = "typeVoieEtablissement"
UNITE_LEGALE = "uniteLegale"
VOIE = "libelleVoieEtablissement"

SIRET_API_REQUEST_FIELDS = [
    ACTIVITE_NAF,
    CODE_INSEE,
    CODE_POSTAL,
    COMMUNE,
    COMPLEMENT,
    DATE_DEBUT,
    ETAT_ETABLISSEMENT,
    INDICE,
    NOM_ENSEIGNE1,
    NOM_ENSEIGNE2,
    NOM_ENSEIGNE3,
    NUMERO,
    PERSONNE_NOM,
    PERSONNE_PRENOM,
    RAISON_SOCIALE,
    SIRET,
    STATUT,
    TYPE_VOIE,
    VOIE,
]

logger = logging.getLogger(__name__)


class Fuzzy(criteria.Field):
    @property
    def representation(self):
        term = str(self.value).replace('"', "").strip()
        if " " in term or "'" in term or "-" in term:
            return f'{self.name}:"{term}"~'
        return f"{self.name}:{term}~"


class OrGroup(criteria.Base):
    "See https://github.com/ln-nicolas/api_insee/issues/3"

    def __init__(self, *criteria, **kwargs):
        self.criteria_list = criteria

    def toURLParams(self):
        inner = " OR ".join([ct.toURLParams() for ct in self.criteria_list])
        return f"({inner})"


def get_client():
    try:
        return ApiInsee(
            key=settings.INSEE_API_CLIENT_KEY,
            secret=settings.INSEE_API_SECRET_KEY,
        )
    except HTTPError as err:
        logger.warn(err)
        raise RuntimeError("Le service INSEE est indisponible.")
    except Exception:
        # api_insee raise standard exceptions when unable to connect to the auth service ;(
        raise RuntimeError("Le service INSEE est inaccessible.")


def format_siret(value, separator=""):
    return siret.format(value, separator=separator)


def extract_etablissement_nom(etablissement):
    nom_parts = []
    uniteLegale = etablissement.get(UNITE_LEGALE, {})
    nom_parts.append(uniteLegale.get(NOM_ENSEIGNE3))
    # périodes et résolution du nom
    periodesEtablissement = etablissement.get(PERIODES_ETABLISSEMENT, [])
    if len(periodesEtablissement) > 0:
        nom_parts.append(periodesEtablissement[0].get(NOM_ENSEIGNE1))
        nom_parts.append(periodesEtablissement[0].get(NOM_ENSEIGNE2))
    nom_parts.append(uniteLegale.get(RAISON_SOCIALE))
    nom_parts.append(
        " ".join(
            [
                uniteLegale.get(PERSONNE_NOM) or "",
                uniteLegale.get(PERSONNE_PRENOM) or "",
            ]
        )
        .strip()
        .title()
    )
    return " ".join(
        sorted(  # required as a set might come randomly sorted
            set([part.title() for part in nom_parts if part is not None and part != ""])
        )
    )


def parse_etablissement(etablissement):
    siret = etablissement.get(SIRET)
    # unité légale
    uniteLegale = etablissement.get(UNITE_LEGALE)
    naf = uniteLegale.get(ACTIVITE_NAF)
    # adresse
    adresseEtablissement = etablissement.get("adresseEtablissement")
    numeroVoieEtablissement = adresseEtablissement.get(NUMERO)
    indiceRepetitionEtablissement = adresseEtablissement.get(INDICE)
    typeVoieEtablissement = adresseEtablissement.get(TYPE_VOIE)
    if typeVoieEtablissement and typeVoieEtablissement in TYPES_VOIE:
        typeVoieEtablissement = TYPES_VOIE.get(typeVoieEtablissement)
    libelleVoieEtablissement = adresseEtablissement.get(VOIE)
    # état
    actif = uniteLegale.get(STATUT) == "A"
    closed_on = None
    periodesEtablissement = etablissement.get(PERIODES_ETABLISSEMENT, [])
    if len(periodesEtablissement) > 0:
        dernierePeriode = periodesEtablissement[0]
        if dernierePeriode.get(ETAT_ETABLISSEMENT) == "F":
            actif = False
            closed_on = dernierePeriode.get(DATE_DEBUT)

    return dict(
        source="sirene",
        source_id=siret,
        actif=actif,
        closed_on=closed_on,
        coordonnees=None,
        naf=naf,
        activite=None,  # XXX would be nice to infer an activity from naf code
        nom=extract_etablissement_nom(etablissement),
        siret=siret,
        numero=" ".join(
            [
                numeroVoieEtablissement or "",
                indiceRepetitionEtablissement or "",
            ]
        ).strip()
        or None,
        voie=" ".join(
            [
                typeVoieEtablissement or "",
                libelleVoieEtablissement or "",
            ]
        ).strip()
        or None,
        lieu_dit=adresseEtablissement.get(COMPLEMENT),
        code_postal=adresseEtablissement.get(CODE_POSTAL),
        commune=adresseEtablissement.get(COMMUNE),
        code_insee=adresseEtablissement.get(CODE_INSEE),
        contact_email=None,
        telephone=None,
        site_internet=None,
    )


def extract_http_error_message(err):
    try:
        decoded = json.loads(err.read().decode())
        return decoded["header"]["message"]
    except (json.decoder.JSONDecodeError, KeyError):
        return


def execute_request(request):
    logger.info(f"Sirene query: {request.url}")
    try:
        return request.get()
    except HTTPError as err:
        error_msg = extract_http_error_message(err)
        if err.code == 403:
            raise RuntimeError(f"Interdit: {error_msg}")
        if err.code == 404:
            raise RuntimeError("Aucun résultat.")
        elif err.code == 400:
            logger.error(f"Requête SIRENE malformée : {error_msg}")
            raise RuntimeError("Recherche malformée.")
        else:
            logger.error(f"Service INSEE indisponible: {error_msg}")
            raise RuntimeError("Le service INSEE est indisponible.")
    except RequestExeption as err:
        logger.error(err)
        raise RuntimeError(f"Recherche impossible: {err}")


def create_find_query(nom, lieu, naf=None):
    query = (
        criteria.Field(STATUT, "A")
        & OrGroup(
            criteria.FieldExact(CODE_POSTAL, lieu),
            Fuzzy(COMMUNE, lieu),
        )
        & OrGroup(
            Fuzzy(RAISON_SOCIALE, nom.upper()),
            Fuzzy(NOM_ENSEIGNE3, nom.upper()),
            Fuzzy(PERSONNE_NOM, nom.upper()),
            criteria.Periodic(Fuzzy(NOM_ENSEIGNE1, nom.upper())),
            criteria.Periodic(Fuzzy(NOM_ENSEIGNE2, nom.upper())),
        )
    )
    if naf:
        query = query & criteria.Field(ACTIVITE_NAF, f"{naf}~")
    return query


def find_etablissements(nom, code_postal, naf=None, limit=10):
    q = create_find_query(nom, code_postal, naf=naf)
    request = get_client().siret(
        q=q,
        nombre=limit,
        masquerValeursNulles=True,
    )
    response = execute_request(request)
    results = []
    for etablissement in response.get("etablissements", []):
        results.append(parse_etablissement(etablissement))
    if len(results) == 0:
        raise RuntimeError("Aucun résultat")
    return results


def get_siret_info(value):
    request = get_client().siret(
        value,
        champs=SIRET_API_REQUEST_FIELDS,
    )
    response = execute_request(request)
    return parse_etablissement(response.get("etablissement"))


def validate_siret(value):
    try:
        return siret.validate(value)
    except stdnum_ex.ValidationError:
        return None
