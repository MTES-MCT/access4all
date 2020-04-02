ACCESSIBILITE_SCHEMA = {
    "stationnement": {
        "label": "Stationnement",
        "fields": [
            "stationnement_presence",
            "stationnement_pmr",
            "stationnement_ext_presence",
            "stationnement_ext_pmr",
        ],
    },
    "cheminement_ext": {
        "label": "Cheminement extérieur",
        "fields": [
            "cheminement_ext_plain_pied",
            "cheminement_ext_nombre_marches",
            "cheminement_ext_reperage_marches",
            "cheminement_ext_main_courante",
            "cheminement_ext_rampe",
            "cheminement_ext_ascenseur",
            "cheminement_ext_pente",
            "cheminement_ext_devers",
            "cheminement_ext_bande_guidage",
            "cheminement_ext_guidage_sonore",
            "cheminement_ext_retrecissement",
        ],
    },
    "entree": {
        "label": "Entrée",
        "fields": [
            "entree_reperage",
            "entree_vitree",
            "entree_vitree_vitrophanie",
            "entree_plain_pied",
            "entree_marches",
            "entree_marches_reperage",
            "entree_marches_main_courante",
            "entree_marches_rampe",
            "entree_dispositif_appel",
            "entree_aide_humaine",
            "entree_ascenseur",
            "entree_largeur_mini",
            "entree_pmr",
            "entree_pmr_informations",
        ],
    },
    "accueil": {
        "label": "Accueil",
        "fields": [
            "accueil_visibilite",
            "accueil_personnels",
            "accueil_equipements_malentendants",
            "accueil_cheminement_plain_pied",
            "accueil_cheminement_nombre_marches",
            "accueil_cheminement_reperage_marches",
            "accueil_cheminement_main_courante",
            "accueil_cheminement_rampe",
            "accueil_cheminement_ascenseur",
            "accueil_retrecissement",
            "accueil_prestations",
        ],
    },
    "labels": {
        "label": "Labels",
        "fields": ["labels", "labels_familles_handicap", "labels_autre",],
    },
    "sanitaires": {
        "label": "Sanitaires",
        "fields": ["sanitaires_presence", "sanitaires_adaptes",],
    },
    "commentaire": {"label": "Commentaire", "fields": ["commentaire"],},
}


def get_accessibilite_admin_schema():
    schema = {}
    for section_id, section_data in ACCESSIBILITE_SCHEMA.items():
        schema[section_data["label"]] = {"fields": section_data["fields"]}
    return list(schema.items())


def get_accessibilite_api_schema():
    return ACCESSIBILITE_SCHEMA