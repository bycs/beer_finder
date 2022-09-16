from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from server.settings import DEBUG
from server.settings import MEDIA_ROOT
from server.settings import MEDIA_URL
from server.settings import STATIC_ROOT
from server.settings import STATIC_URL


urlpatterns: list = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("beers.urls")),
]


if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
