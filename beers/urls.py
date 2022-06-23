from django.urls import path

from . import views

urlpatterns = [
    path("sync_all_beers/", views.sync_all_beers, name="sync_all_beers"),
]
