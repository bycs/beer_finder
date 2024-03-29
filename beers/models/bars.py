import uuid

from django.db import models

from beers.logics.geo import YandexMapGeo


class Bar(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")
    website = models.URLField(unique=True, verbose_name="Website")
    updated = models.DateTimeField(null=True, default=None, blank=True, verbose_name="Updated")

    class Meta:
        ordering = ("name",)
        verbose_name = "Bar"
        verbose_name_plural = "Bars"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Bar: {self.name}>"


class BarBranch(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE, verbose_name="Bar")
    address = models.CharField(max_length=255, null=False, verbose_name="Address")
    metro = models.CharField(
        max_length=255, null=True, default=None, blank=True, verbose_name="Metro"
    )
    latitude = models.FloatField(null=True, default=None, blank=True, verbose_name="Latitude")
    longitude = models.FloatField(null=True, default=None, blank=True, verbose_name="Longitude")

    @property
    def bar_branch_name(self) -> str:
        return f"{self.bar.name} - {self.metro}"

    bar_branch_name.fget.short_description = "BarBranch Name"  # type: ignore[attr-defined]

    @property
    def point(self) -> str:
        if (self.latitude is None or self.longitude is None) and self.address is not None:
            self.get_geocode()
        return f"{self.latitude},{self.longitude}"

    point.fget.short_description = "Point"  # type: ignore[attr-defined]

    class Meta:
        ordering = ("bar", "metro")
        verbose_name = "BarBranch"
        verbose_name_plural = "BarBranches"

    def __str__(self) -> str:
        return f"{self.bar_branch_name}"

    def __repr__(self) -> str:
        return f"<BarBranch: {self.bar_branch_name}>"

    def get_geocode(self) -> None:
        geo = YandexMapGeo()
        point = geo.geocode(address=self.address)
        if point is not None:
            self.latitude = point.latitude
            self.longitude = point.longitude
            self.save()
            print(f"Geocode for {self.address} is {point}")
