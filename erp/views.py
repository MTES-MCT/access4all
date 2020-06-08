from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

from .forms import (
    PublicErpForm,
    PublicEtablissementSearchForm,
    PublicSiretSearchForm,
    ViewAccessibiliteForm,
)
from .models import Activite, Commune, Erp
from .serializers import SpecialErpSerializer
from . import sirene


def handler403(request, exception):
    return render(request, "403.html", context={"exception": exception}, status=403,)


def handler404(request, exception):
    return render(request, "404.html", context={"exception": exception}, status=404,)


def handler500(request):
    return render(request, "500.html", context={}, status=500)


def home(request):
    communes_qs = Commune.objects.erp_stats()[:12]
    latest = (
        Erp.objects.published()
        .geolocated()
        .select_related("activite", "commune_ext")
        .having_an_accessibilite()
        .order_by("-created_at")[:17]
    )
    search_results = None
    search = request.GET.get("q")
    if search and len(search) > 0:
        erp_qs = (
            Erp.objects.published()
            .geolocated()
            .select_related("accessibilite", "activite", "commune_ext")
            .search(search)
        )
        if request.GET.get("access") == "1":
            erp_qs = erp_qs.having_an_accessibilite()
        search_results = {
            "communes": Commune.objects.search(search).order_by(
                F("population").desc(nulls_last=True)
            )[:4],
            "erps": erp_qs[:10],
        }
    return render(
        request,
        "index.html",
        context={
            "empty_query": "q" in request.GET and not search,
            "search": search,
            "communes": communes_qs,
            "latest": latest,
            "search_results": search_results,
        },
    )


@cache_page(60 * 15)
def autocomplete(request):
    suggestions = []
    q = request.GET.get("q", "")
    commune_slug = request.GET.get("commune_slug")
    if len(q) < 3:
        return JsonResponse({"suggestions": suggestions})
    qs = Erp.objects.published().geolocated()
    if commune_slug:
        qs = qs.filter(commune_ext__slug=commune_slug)
    qs = qs.search(q)[:7]
    for erp in qs:
        score = (erp.rank + erp.similarity - (erp.distance_nom / 6)) * 60
        score = 10 if score > 10 else score
        suggestions.append(
            {
                "value": erp.nom + ", " + erp.adresse,
                "data": {
                    "score": score,
                    "activite": erp.activite and erp.activite.slug,
                    "url": (
                        erp.get_absolute_url()
                        + "?around="
                        + str(erp.geom.coords[1])
                        + ","
                        + str(erp.geom.coords[0])
                    ),
                },
            }
        )
    suggestions = sorted(suggestions, key=lambda s: s["data"]["score"], reverse=True)
    return JsonResponse({"suggestions": suggestions})


class EditorialView(TemplateView):
    template_name = "editorial/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BaseListView(generic.ListView):
    model = Erp
    queryset = (
        Erp.objects.published()
        .select_related("activite", "accessibilite", "commune_ext")
        .geolocated()
    )
    _commune = None

    @property
    def around(self):
        raw = self.request.GET.get("around")
        if raw is None:
            return
        try:
            rlon, rlat = raw.split(",")
            return (float(rlon), float(rlat))
        except (IndexError, ValueError, TypeError):
            return None

    @property
    def commune(self):
        if self._commune is None:
            self._commune = get_object_or_404(
                Commune.objects.select_related(), slug=self.kwargs["commune"]
            )
        return self._commune

    @property
    def search_terms(self):
        q = self.request.GET.get("q", "").strip()
        if len(q) >= 2:
            return q

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.in_commune(self.commune)
        if self.search_terms is not None:
            queryset = queryset.search(self.search_terms)
        else:
            if "activite_slug" in self.kwargs:
                if self.kwargs["activite_slug"] == "non-categorises":
                    queryset = queryset.filter(activite__isnull=True)
                else:
                    queryset = queryset.filter(
                        activite__slug=self.kwargs["activite_slug"]
                    )
            # FIXME: find a better trick to list erps having an accessibilite first,
            # so we can keep name ordering
            queryset = queryset.order_by("accessibilite")
        if self.around is not None:
            queryset = queryset.nearest(self.around)
        # We can't hammer the pages with too many entries, hard-limiting here
        return queryset[:500]


class App(BaseListView):
    "Static, template-based Web application views."
    template_name = "erps/commune.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["around"] = (
            list(self.around) if self.around is not None else self.around
        )
        context["commune"] = self.commune
        context["commune_json"] = self.commune.toTemplateJson()
        context["search_terms"] = self.search_terms
        context["activites"] = Activite.objects.in_commune(
            self.commune
        ).with_erp_counts()
        if (
            "activite_slug" in self.kwargs
            and self.kwargs["activite_slug"] != "non-categorises"
        ):
            context["current_activite"] = get_object_or_404(
                Activite, slug=self.kwargs["activite_slug"]
            )
        if "erp_slug" in self.kwargs:
            erp = get_object_or_404(
                Erp.objects.select_related("accessibilite").published(),
                slug=self.kwargs["erp_slug"],
            )
            context["erp"] = erp
            if erp.has_accessibilite():
                form = ViewAccessibiliteForm(instance=erp.accessibilite)
                context["accessibilite_data"] = form.get_accessibilite_data()
        serializer = SpecialErpSerializer()
        context["geojson_list"] = serializer.serialize(
            context["object_list"],
            geometry_field="geom",
            use_natural_foreign_keys=True,
            fields=[
                "pk",
                "nom",
                "activite__nom",
                "adresse",
                "absolute_url",
                "has_accessibilite",
            ],
        )
        return context


def mon_compte(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    return render(request, "compte/index.html",)


def mes_erps(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    erps = Erp.objects.select_related(
        "accessibilite", "activite", "commune_ext"
    ).filter(user_id=request.user.pk)
    return render(request, "compte/mes_erps.html", context={"erps": erps},)


def to_betagouv(self):
    return redirect("https://beta.gouv.fr/startups/access4all.html")


@login_required
def contrib_start(request):
    siret_search_error = None
    name_search_error = None
    name_search_results = None
    siret_form = PublicSiretSearchForm()
    name_form = PublicEtablissementSearchForm()
    if request.method == "POST":
        if request.POST.get("type") == "by-name":
            name_form = PublicEtablissementSearchForm(request.POST)
            if name_form.is_valid():
                try:
                    name_search_results = sirene.find_etablissements(
                        name_form.cleaned_data["nom"],
                        name_form.cleaned_data["code_postal"],
                        limit=10,
                    )
                except RuntimeError as err:
                    name_search_error = str(err)
        elif request.POST.get("type") == "by-siret":
            siret_form = PublicSiretSearchForm(request.POST)
            if siret_form.is_valid():
                try:
                    siret_info = sirene.get_siret_info(siret_form.cleaned_data["siret"])
                    data = sirene.base64_encode_etablissement(siret_info)
                    return redirect(reverse("contrib_admin_infos") + "?data=" + data)
                except RuntimeError as err:
                    siret_search_error = err
        else:
            raise RuntimeError("Unsupported action type")
    return render(
        request,
        template_name="contrib/0-start.html",
        context={
            "name_form": name_form,
            "name_search_results": name_search_results,
            "siret_form": siret_form,
            "name_search_error": name_search_error,
            "siret_search_error": siret_search_error,
        },
    )


@login_required
def contrib_admin_infos(request):
    data = None
    data_error = None
    if request.method == "POST":
        form = PublicErpForm(request.POST)
        if form.is_valid():
            raise RuntimeError("TODO: form is ok, what next?")
    else:
        data = request.GET.get("data")
        if data is not None:
            try:
                data = sirene.base64_decode_etablissement(data)
            except RuntimeError as err:
                data_error = err
        form = PublicErpForm(data)
    return render(
        request,
        template_name="contrib/1-admin-infos.html",
        context={"form": form, "has_data": data is not None, "data_error": data_error},
    )
