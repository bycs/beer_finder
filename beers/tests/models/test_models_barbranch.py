import uuid

from django.test import TestCase

from beers.models.bars import Bar
from beers.models.bars import BarBranch


class BarBranchModelTest(TestCase):
    barbranch: BarBranch

    @classmethod
    def setUpTestData(cls) -> None:
        bar = Bar.objects.create(
            pk=uuid.UUID("c4f516a7-33e9-41f5-ab2f-2a2b732b92f5"),
            name="Bar #1",
            website="https://bar1.com",
        )
        cls.create = BarBranch.objects.create(
            pk=uuid.UUID("5485f666-dc40-4c35-b529-047715269bd6"),
            bar=bar,
            address="Россия, Москва",
            metro="Октябрьская",
        )
        barbranch = cls.create

        cls.barbranch = barbranch

    def test_model_bar_it_has_fields(self) -> None:
        self.assertIsInstance(self.barbranch.bar, Bar)
        self.assertIsInstance(self.barbranch.address, str)
        self.assertIsInstance(self.barbranch.metro, str)
        self.assertIsInstance(self.barbranch.latitude, float | None)
        self.assertIsInstance(self.barbranch.longitude, float | None)

    def test_model_barbranch_bar_label(self) -> None:
        barbranch = BarBranch.objects.get(pk="5485f666-dc40-4c35-b529-047715269bd6")
        field_label = barbranch._meta.get_field("bar").verbose_name
        self.assertEqual(field_label, "Bar")

    def test_model_barbranch_address_label(self) -> None:
        barbranch = BarBranch.objects.get(pk="5485f666-dc40-4c35-b529-047715269bd6")
        field_label = barbranch._meta.get_field("address").verbose_name
        self.assertEqual(field_label, "Address")

    def test_model_barbranch_metro_label(self) -> None:
        barbranch = BarBranch.objects.get(pk="5485f666-dc40-4c35-b529-047715269bd6")
        field_label = barbranch._meta.get_field("metro").verbose_name
        self.assertEqual(field_label, "Metro")

    def test_model_barbranch_latitude_label(self) -> None:
        barbranch = BarBranch.objects.get(pk="5485f666-dc40-4c35-b529-047715269bd6")
        field_label = barbranch._meta.get_field("latitude").verbose_name
        self.assertEqual(field_label, "Latitude")

    def test_model_barbranch_longitude_label(self) -> None:
        barbranch = BarBranch.objects.get(pk="5485f666-dc40-4c35-b529-047715269bd6")
        field_label = barbranch._meta.get_field("longitude").verbose_name
        self.assertEqual(field_label, "Longitude")

    def test_model_barbranch_address_max_length(self) -> None:
        barbranch = BarBranch.objects.get(pk="5485f666-dc40-4c35-b529-047715269bd6")
        max_length = barbranch._meta.get_field("address").max_length
        self.assertEqual(max_length, 255)

    def test_model_barbranch_metro_max_length(self) -> None:
        barbranch = BarBranch.objects.get(pk="5485f666-dc40-4c35-b529-047715269bd6")
        max_length = barbranch._meta.get_field("metro").max_length
        self.assertEqual(max_length, 255)

    def test_model_barbranch_object_name(self) -> None:
        barbranch = BarBranch.objects.get(pk="5485f666-dc40-4c35-b529-047715269bd6")
        expected_object_name = "%s - %s" % (barbranch.bar.name, barbranch.metro)
        self.assertEqual(expected_object_name, str(barbranch))

    def test_model_barbranch_object_repr(self) -> None:
        barbranch = BarBranch.objects.get(pk="5485f666-dc40-4c35-b529-047715269bd6")
        expected_object_repr = "<BarBranch: %s - %s>" % (barbranch.bar.name, barbranch.metro)
        self.assertEqual(expected_object_repr, repr(barbranch))
