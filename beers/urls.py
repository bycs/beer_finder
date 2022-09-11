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
    path("top_spec_beers/", views.top_spec_beers, name="top_spec_beers"),
    path("sync_all_beers/", views.sync_all_beers, name="sync_all_beers"),
]
