from django.db import models

from beers.logics.geo import YandexMapGeo


class Bar(models.Model):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(unique=True)
    updated = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Bar: {self.name}>"


class BarBranch(models.Model):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, unique=True)
    metro = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, default=None)
    longitude = models.FloatField(null=True, default=None)

    @property
    def bar_branch_name(self):
        return f"{self.bar.name} - {self.metro}"

    @property
    def point(self):
        if (self.latitude is None or self.longitude is None) and self.address is not None:
            self.get_geocode()
        return f"{self.latitude},{self.longitude}"

    def __str__(self):
        return f"{self.bar.name} - {self.metro}"

    def __repr__(self):
        return f"<BarBranch: {self.bar.name} - {self.metro}>"

    def get_geocode(self) -> None:
        geo = YandexMapGeo()
        point = geo.geocode(address=self.address)
        if point is not None:
            self.latitude = point.latitude
            self.longitude = point.longitude
            self.save()
            print(f"Geocode for {self.address} is {point}")
