from django.db import models

from beers.managers.beers import BeerManager
from beers.models.bars import Bar


class Beer(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True)
    description = models.TextField(null=True)
    specifications = models.JSONField(default=dict, null=True)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)

    @property
    def price_rub(self):
        if self.price is None:
            return None
        return self.price / 100

    objects = BeerManager()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Beer: {self.name}>"
