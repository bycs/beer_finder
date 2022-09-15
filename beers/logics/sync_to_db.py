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
