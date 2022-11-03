from django.conf.urls.static import static
from django.contrib import admin
<<<<<<< HEAD
from django.urls import include, path
=======
from django.urls import include
from django.urls import path
>>>>>>> 574b7bc1525c9d3a1f77fe4fda3c0220ed8f629f

from server.settings import DEBUG
from server.settings import MEDIA_ROOT
from server.settings import MEDIA_URL
from server.settings import STATIC_ROOT
from server.settings import STATIC_URL


urlpatterns: list = [
    path("admin/", admin.site.urls),
<<<<<<< HEAD
    path("", include("beers.urls")),
=======
    path("api/v1/", include("beers.urls")),
>>>>>>> 574b7bc1525c9d3a1f77fe4fda3c0220ed8f629f
]


if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
