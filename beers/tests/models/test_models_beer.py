from django.test import TestCase

from beers.models.bars import Bar
from beers.models.beers import Beer


class BeerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        bar = Bar.objects.create(name="Bar #1", website="https://bar1.com")
        Beer.objects.create(
            name="Beer #1",
            price=100000,
            bar=bar,
            description="Beer #1 description",
            specifications={"alcohol": 5.5},
        )

    def test_model_beer_name_label(self):
        beer = Beer.objects.get(pk=1)
        field_label = beer._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "Name")

    def test_model_beer_price_label(self):
        beer = Beer.objects.get(pk=1)
        field_label = beer._meta.get_field("price").verbose_name
        self.assertEquals(field_label, "Price")

    def test_model_beer_bar_label(self):
        beer = Beer.objects.get(pk=1)
        field_label = beer._meta.get_field("bar").verbose_name
        self.assertEquals(field_label, "Bar")

    def test_model_beer_description_label(self):
        beer = Beer.objects.get(pk=1)
        field_label = beer._meta.get_field("description").verbose_name
        self.assertEquals(field_label, "Description")

    def test_model_beer_specifications_label(self):
        beer = Beer.objects.get(pk=1)
        field_label = beer._meta.get_field("specifications").verbose_name
        self.assertEquals(field_label, "Specifications")

    def test_model_beer_name_max_length(self):
        beer = Beer.objects.get(pk=1)
        max_length = beer._meta.get_field("name").max_length
        self.assertEquals(max_length, 255)

    def test_model_beer_object_name(self):
        beer = Beer.objects.get(pk=1)
        expected_object_name = "%s" % (beer.name)
        self.assertEquals(expected_object_name, str(beer))

    def test_model_beer_object_repr(self):
        beer = Beer.objects.get(pk=1)
        expected_object_name = "<Beer: %s>" % (beer.name)
        self.assertEquals(expected_object_name, repr(beer))
