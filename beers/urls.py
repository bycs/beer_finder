from django.urls import include, path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"beers", views.BeersViewSet, basename="beers")
router.register(r"bars", views.BarsViewSet, basename="bars")
router.register(r"bar_branches", views.BarBranchesViewSet, basename="bar_branches")

urlpatterns = [
    path("", include(router.urls)),
    path("sync_all_beers/", views.sync_all_beers, name="sync_all_beers"),
]
