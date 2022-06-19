from django.db import models


class Bar(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Bar: {self.name}>"


class BarBranch(models.Model):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    metro = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.bar.name} - {self.metro}"

    def __repr__(self):
        return f"<BarBranch: {self.bar.name} - {self.metro}>"


class Beer(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    specifications = models.JSONField(default=dict)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Beer: {self.name}>"
