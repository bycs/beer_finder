from beers.models.beers import Beer
from beers.parsers.lambic import base_url, get_all_beers_lambic, list_urls_for_parce
from beers.parsers.we_cidreria import get_beers_we_cidreria


def sync_lambic():
    beers = get_all_beers_lambic(base_url, list_urls_for_parce)
    Beer.beer_managers.sync_bar_beers_to_db("Lambic", beers)


def sync_we_cidreria():
    beers = get_beers_we_cidreria()
    Beer.beer_managers.sync_bar_beers_to_db("We Cidreria", beers)
