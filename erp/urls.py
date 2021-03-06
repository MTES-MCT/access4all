from django.contrib.auth import views as auth_views
from django.urls import path, include

from core.cache import cache_per_user
from erp import schema, views

APP_CACHE_TTL = 60 * 5
EDITORIAL_CACHE_TTL = 60 * 60


handler403 = views.handler403
handler404 = views.handler404
handler500 = views.handler500


def cache_app_page():
    return cache_per_user(APP_CACHE_TTL)(views.App.as_view())


def cache_user_page(view):
    return cache_per_user(APP_CACHE_TTL)(view)


def cache_editorial_page(template_name, context=None):
    return cache_per_user(EDITORIAL_CACHE_TTL)(
        views.EditorialView.as_view(template_name=template_name, extra_context=context)
    )


urlpatterns = [
    path("mapicons", views.mapicons, name="mapicons"),
    ############################################################################
    # Editorial
    ############################################################################
    path(
        "",
        cache_user_page(views.home),
        name="home",
    ),
    path(
        "conditions-generales-d-utilisation",
        cache_editorial_page("editorial/cgu.html"),
        name="cgu",
    ),
    path(
        "accessibilite",
        cache_editorial_page("editorial/accessibilite.html"),
        name="accessibilite",
    ),
    path(
        "partenaires",
        cache_editorial_page(
            "editorial/partenaires.html", context={"partenaires": schema.PARTENAIRES}
        ),
        name="partenaires",
    ),
    ############################################################################
    # HTML app
    ############################################################################
    path(
        "app/autocomplete/",
        views.autocomplete,
        name="autocomplete",
    ),
    path(
        "communes/",
        cache_user_page(views.communes),
        name="communes",
    ),
    path(
        "recherche/",
        cache_user_page(views.search),
        name="search",
    ),
    path(
        "app/<str:commune>/",
        cache_app_page(),
        name="commune",
    ),
    path(
        "app/<str:commune>/a/<str:activite_slug>/",
        cache_app_page(),
        name="commune_activite",
    ),
    path(
        "app/<str:commune>/erp/<str:erp_slug>/",
        views.App.as_view(),  # avoid caching details page
        name="commune_erp",
    ),
    path(
        "app/<str:commune>/a/<str:activite_slug>/erp/<str:erp_slug>/",
        views.App.as_view(),  # avoid caching details page
        name="commune_activite_erp",
    ),
    path("app/<str:erp_slug>/vote/", views.vote, name="erp_vote"),
    ############################################################################
    # Account
    ############################################################################
    path("mon_compte/", views.mon_compte, name="mon_compte"),
    path("mon_compte/erps/", views.mes_erps, name="mes_erps"),
    path("mon_compte/abonnements/", views.mes_abonnements, name="mes_abonnements"),
    path("mon_compte/identifiant/", views.mon_identifiant, name="mon_identifiant"),
    path(
        "mon_compte/contributions/", views.mes_contributions, name="mes_contributions"
    ),
    path(
        "mon_compte/contributions/recues/",
        views.mes_contributions_recues,
        name="mes_contributions_recues",
    ),
    ############################################################################
    # Ajout ERP
    ############################################################################
    path("contrib/delete/<str:erp_slug>/", views.contrib_delete, name="contrib_delete"),
    path("contrib/start/", views.contrib_start, name="contrib_start"),
    path(
        "contrib/start/recherche/",
        views.contrib_global_search,
        name="contrib_global_search",
    ),
    path("contrib/claim/<str:erp_slug>/", views.contrib_claim, name="contrib_claim"),
    path("contrib/admin-infos/", views.contrib_admin_infos, name="contrib_admin_infos"),
    path(
        "contrib/edit-infos/<str:erp_slug>/",
        views.contrib_edit_infos,
        name="contrib_edit_infos",
    ),
    path(
        "contrib/localisation/<str:erp_slug>/",
        views.contrib_localisation,
        name="contrib_localisation",
    ),
    path(
        "contrib/transport/<str:erp_slug>/",
        views.contrib_transport,
        name="contrib_transport",
    ),
    path(
        "contrib/stationnement/<str:erp_slug>/",
        views.contrib_stationnement,
        name="contrib_stationnement",
    ),
    path(
        "contrib/exterieur/<str:erp_slug>/",
        views.contrib_exterieur,
        name="contrib_exterieur",
    ),
    path(
        "contrib/entree/<str:erp_slug>/",
        views.contrib_entree,
        name="contrib_entree",
    ),
    path(
        "contrib/accueil/<str:erp_slug>/",
        views.contrib_accueil,
        name="contrib_accueil",
    ),
    path(
        "contrib/sanitaires/<str:erp_slug>/",
        views.contrib_sanitaires,
        name="contrib_sanitaires",
    ),
    path(
        "contrib/labellisation/<str:erp_slug>/",
        views.contrib_labellisation,
        name="contrib_labellisation",
    ),
    path(
        "contrib/commentaire/<str:erp_slug>/",
        views.contrib_commentaire,
        name="contrib_commentaire",
    ),
    path(
        "contrib/publication/<str:erp_slug>/",
        views.contrib_publication,
        name="contrib_publication",
    ),
    ############################################################################
    # Admin stuff
    ############################################################################
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="admin_password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="admin_password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="admin_password_reset_complete",
    ),
    path("nested_admin/", include("nested_admin.urls")),
]
