from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r"bars", views.BarsViewSet, basename="bars")
router.register(r"bar_branches", views.BarBranchesViewSet, basename="bar_branches")
router.register(r"beers", views.BeersViewSet, basename="beers")
router.register(r"filter_beers", views.FilterBeersViewSet, basename="filter_beers")
router.register(r"top_spec_beers_v1", views.TopSpecV1ViewSet, basename="top_spec_beers_v1")
router.register(r"top_spec_beers_v2", views.TopSpecV2ViewSet, basename="top_spec_beers_v2")

urlpatterns = [
    path("", include(router.urls)),
    path("sync_all_beers/", views.sync_all_beers, name="sync_all_beers"),
    path("openapi/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
