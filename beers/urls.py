from django.urls import include, path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"", views.BeersViewSet, basename="beers")

urlpatterns = [
    path("", include(router.urls)),
    path("sync_all_beers/", views.sync_all_beers, name="sync_all_beers"),
]
