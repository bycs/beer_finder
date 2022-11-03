<<<<<<< HEAD
from beers.models.beers import Beer
from beers.parsers.lambic import base_url, get_all_beers_lambic, list_urls_for_parce
from beers.parsers.we_cidreria import get_beers_we_cidreria
from beers.parsers.we_pub import get_beers_we_pub


def sync_lambic():
    beers = get_all_beers_lambic(base_url, list_urls_for_parce)
    Beer.beer_managers.sync_bar_beers_to_db("Lambic", beers)


def sync_we_cidreria():
    beers = get_beers_we_cidreria()
    Beer.beer_managers.sync_bar_beers_to_db("We Cidreria", beers)


def sync_we_pub():
    beers = get_beers_we_pub()
    Beer.beer_managers.sync_bar_beers_to_db("WE Pub", beers)
=======
from beers.parsers.lambic import Lambic
from beers.parsers.we_cidreria import WeCidreria
from beers.parsers.we_pub import WePub


def sync_lambic():
    lambic = Lambic()
    lambic.run()


def sync_we_cidreria():
    we_cidreria = WeCidreria()
    we_cidreria.run()


def sync_we_pub():
    we_pub = WePub()
    we_pub.run()
>>>>>>> 574b7bc1525c9d3a1f77fe4fda3c0220ed8f629f
