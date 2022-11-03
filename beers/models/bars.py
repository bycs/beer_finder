from django.db import models

from beers.logics.geo import YandexMapGeo


class Bar(models.Model):
<<<<<<< HEAD
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(unique=True)
    updated = models.DateTimeField(null=True, default=None)
=======
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")
    website = models.URLField(unique=True, verbose_name="Website")
    updated = models.DateTimeField(null=True, default=None, verbose_name="Updated")

    class Meta:
        ordering = ("name",)
        verbose_name = "Bar"
        verbose_name_plural = "Bars"
>>>>>>> 574b7bc1525c9d3a1f77fe4fda3c0220ed8f629f

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Bar: {self.name}>"


class BarBranch(models.Model):
<<<<<<< HEAD
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, unique=True)
    metro = models.CharField(max_length=255)

    @property
    def bar_branch_name(self):
        return f"{self.bar.name} - {self.metro}"

    def __str__(self):
=======
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE, verbose_name="Bar")
    address = models.CharField(max_length=255, unique=True, verbose_name="Address")
    metro = models.CharField(max_length=255, verbose_name="Metro")
    latitude = models.FloatField(null=True, default=None, verbose_name="Latitude")
    longitude = models.FloatField(null=True, default=None, verbose_name="Longitude")

    @property
    def barbranch_name(self) -> str:
>>>>>>> 574b7bc1525c9d3a1f77fe4fda3c0220ed8f629f
        return f"{self.bar.name} - {self.metro}"

    barbranch_name.fget.short_description = "BarBranch Name"  # type: ignore [attr-defined]

    @property
    def point(self) -> str:
        if (self.latitude is None or self.longitude is None) and self.address is not None:
            self.get_geocode()
        return f"{self.latitude},{self.longitude}"

    point.fget.short_description = "Point"  # type: ignore [attr-defined]

    class Meta:
        ordering = ("bar", "metro")
        verbose_name = "BarBranch"
        verbose_name_plural = "BarBranches"

    def __str__(self) -> str:
        return f"{self.barbranch_name}"

    def __repr__(self) -> str:
        return f"<BarBranch: {self.barbranch_name}>"

    def get_geocode(self) -> None:
        geo = YandexMapGeo()
        point = geo.geocode(address=self.address)
        if point is not None:
            self.latitude = point.latitude
            self.longitude = point.longitude
            self.save()
            print(f"Geocode for {self.address} is {point}")
