from datetime import datetime

from django.db import models
from django.db import transaction

from beers.models.bars import Bar


class BeerManager(models.Manager):
    def sync_bar_beers_to_db(self, bar_name: str, beers: list[dict]) -> None:
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
        current_bar.updated = datetime.now()
        with transaction.atomic():
            self.filter(bar=current_bar.pk).delete()
            self.bulk_create(objs)
            current_bar.save()
