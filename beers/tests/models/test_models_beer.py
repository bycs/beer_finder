import uuid

from django.test import TestCase

from beers.models.bars import Bar
from beers.models.beers import Beer


class BeerModelTest(TestCase):
    beer: Beer

    @classmethod
    def setUpTestData(cls) -> None:
        bar = Bar.objects.create(
            pk=uuid.UUID("c4f516a7-33e9-41f5-ab2f-2a2b732b92f5"),
            name="Bar #1",
            website="https://bar1.com",
        )
        beer = Beer.objects.create(
            pk=uuid.UUID("44842e77-d995-4464-b3bb-f92cfa3b9065"),
            name="Beer #1",
            price=100000,
            bar=bar,
            description="Beer #1 description",
            specifications={"alcohol": 5.5},
        )

        cls.beer = beer

    def test_model_bar_it_has_fields(self) -> None:
        self.assertIsInstance(self.beer.name, str)
        self.assertIsInstance(self.beer.price, int | None)
        self.assertIsInstance(self.beer.description, str | None)
        self.assertIsInstance(self.beer.specifications, dict | None)
        self.assertIsInstance(self.beer.bar, Bar)

    def test_model_beer_name_label(self) -> None:
        beer = Beer.objects.get(pk="44842e77-d995-4464-b3bb-f92cfa3b9065")
        field_label = beer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Name")

    def test_model_beer_price_label(self) -> None:
        beer = Beer.objects.get(pk="44842e77-d995-4464-b3bb-f92cfa3b9065")
        field_label = beer._meta.get_field("price").verbose_name
        self.assertEqual(field_label, "Price")

    def test_model_beer_bar_label(self) -> None:
        beer = Beer.objects.get(pk="44842e77-d995-4464-b3bb-f92cfa3b9065")
        field_label = beer._meta.get_field("bar").verbose_name
        self.assertEqual(field_label, "Bar")

    def test_model_beer_description_label(self) -> None:
        beer = Beer.objects.get(pk="44842e77-d995-4464-b3bb-f92cfa3b9065")
        field_label = beer._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "Description")

    def test_model_beer_specifications_label(self) -> None:
        beer = Beer.objects.get(pk="44842e77-d995-4464-b3bb-f92cfa3b9065")
        field_label = beer._meta.get_field("specifications").verbose_name
        self.assertEqual(field_label, "Specifications")

    def test_model_beer_name_max_length(self) -> None:
        beer = Beer.objects.get(pk="44842e77-d995-4464-b3bb-f92cfa3b9065")
        max_length = beer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_model_beer_object_name(self) -> None:
        beer = Beer.objects.get(pk="44842e77-d995-4464-b3bb-f92cfa3b9065")
        expected_object_name = "%s" % (beer.name)
        self.assertEqual(expected_object_name, str(beer))

    def test_model_beer_object_repr(self) -> None:
        beer = Beer.objects.get(pk="44842e77-d995-4464-b3bb-f92cfa3b9065")
        expected_object_name = "<Beer: %s>" % (beer.name)
        self.assertEqual(expected_object_name, repr(beer))
