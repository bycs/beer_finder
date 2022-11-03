from django.db import models

from beers.managers.beers import BeerManager
from beers.models.bars import Bar


class Beer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    price = models.IntegerField(null=True, default=None, verbose_name="Price")
    description = models.TextField(null=True, default=None, verbose_name="Description")
    specifications = models.JSONField(default=dict, null=True, verbose_name="Specifications")
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE, verbose_name="Bar")

    @property
    def price_rub(self) -> int | None:
        if self.price is None:
            return None
        return int(self.price / 100)

    price_rub.fget.short_description = "Price Rub"  # type: ignore [attr-defined]

    objects = BeerManager()

<<<<<<< HEAD
    @property
    def price_rub(self):
        return self.price / 100

    beer_managers = BeerManager()
=======
    class Meta:
        ordering = ("name", "bar")
        verbose_name = "Beer"
        verbose_name_plural = "Beers"
>>>>>>> 574b7bc1525c9d3a1f77fe4fda3c0220ed8f629f

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Beer: {self.name}>"
