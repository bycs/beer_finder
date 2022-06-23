from beers.models.bars import Bar

from django.db import models, transaction


class BeerManager(models.Manager):
    def sync_bar_beers_to_db(self, bar_name: int, beers: list):
        current_bar = Bar.objects.get(name=bar_name)
        objs = [
            self.model(
                name=beer["name"],
                price=beer["price"],
                description=beer["description"],
                specifications=beer["specifications"],
                bar=current_bar,
            )
            for beer in beers
        ]
        with transaction.atomic():
            self.filter(bar=current_bar.pk).delete()
            self.bulk_create(objs)
