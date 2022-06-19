from beers.models import Bar

from django.db import models, transaction


class BeerManager(models.Manager):
    def sync_bar_beers_to_db(self, bar_id: int, beers: list):
        bar_id = Bar.objects.get(name=bar_id).pk
        objs = [
            self.model(
                name=beer["name"],
                price=beer["price"],
                description=beer["description"],
                specifications=beer["specifications"],
                bar=bar_id,
            )
            for beer in beers
        ]
        with transaction.atomic():
            self.filter(self.bar == bar_id).delete()
            self.bulk_create(objs)
