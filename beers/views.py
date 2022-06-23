from django.http import HttpResponse

from beers.decorators import staff_required
from beers.logics import sync_to_db


@staff_required
def sync_all_beers(request):
    sync_to_db.sync_lambic()
    sync_to_db.sync_we_cidreria()
    return HttpResponse("Все ок!")
