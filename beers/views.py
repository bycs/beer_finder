from beers.decorators import staff_required
from beers.logics import sync_to_db

from django.http import HttpResponse


@staff_required
def sync_all_beers(request):
    sync_to_db.sync_lambic()
    sync_to_db.sync_we_cidreria()
    sync_to_db.sync_we_pub()
    return HttpResponse("Все ок!")
