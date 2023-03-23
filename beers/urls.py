from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework import routers

from beers.views.bars import BarBranchesViewSet
from beers.views.bars import BarsViewSet
from beers.views.base import sync_all_beers
from beers.views.beers import BeersViewSet
from beers.views.beers import TopSpecKeyViewSet


router = routers.DefaultRouter()
router.register(r"bars", BarsViewSet)
router.register(r"bar_branches", BarBranchesViewSet)
router.register(r"beers", BeersViewSet)
router.register(r"top_spec_key_beers", TopSpecKeyViewSet, basename="top_spec_key_beers")

urlpatterns = [
    path("", include(router.urls)),
    path("sync_all_beers/", sync_all_beers, name="sync_all_beers"),
    path("openapi/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
