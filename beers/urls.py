from django.urls import include, path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"beers", views.BeersViewSet, basename="beers")
router.register(r"bars", views.BarsViewSet, basename="bars")
router.register(r"bar_branches", views.BarBranchesViewSet, basename="bar_branches")

urlpatterns = [
    path("", include(router.urls)),
    path("filter_beers/", views.filter_beers, name="filter_beers"),
    path("top_spec_beers_v1/", views.top_spec_beers_v1, name="top_spec_beers_v1"),
    path("top_spec_beers_v2/", views.top_spec_beers_v2, name="top_spec_beers_v2"),
    path("sync_all_beers/", views.sync_all_beers, name="sync_all_beers"),
]
