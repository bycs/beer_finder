from beers.decorators import staff_required
from beers.logics import sync_to_db
from beers.models.beers import Beer
from beers.serializers import BeerSerializer

from django.http import HttpResponse

from rest_framework import viewsets


@staff_required
def sync_all_beers(request):
    sync_to_db.sync_lambic()
    sync_to_db.sync_we_cidreria()
    sync_to_db.sync_we_pub()
    return HttpResponse("Все ок!")


class BeersViewSet(viewsets.ModelViewSet):
    queryset = Beer.beer_managers.all().order_by("name")
    serializer_class = BeerSerializer
