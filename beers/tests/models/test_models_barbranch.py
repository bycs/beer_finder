from django.test import TestCase

from beers.models.bars import Bar
from beers.models.bars import BarBranch


class BarBranchModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        bar = Bar.objects.create(name="Bar #1", website="https://bar1.com")
        BarBranch.objects.create(
            bar=bar,
            address="Россия, Москва",
            metro="Октябрьская",
        )

    def test_model_barbranch_bar_label(self):
        barbranch = BarBranch.objects.get(pk=1)
        field_label = barbranch._meta.get_field("bar").verbose_name
        self.assertEquals(field_label, "Bar")

    def test_model_barbranch_address_label(self):
        barbranch = BarBranch.objects.get(pk=1)
        field_label = barbranch._meta.get_field("address").verbose_name
        self.assertEquals(field_label, "Address")

    def test_model_barbranch_metro_label(self):
        barbranch = BarBranch.objects.get(pk=1)
        field_label = barbranch._meta.get_field("metro").verbose_name
        self.assertEquals(field_label, "Metro")

    def test_model_barbranch_latitude_label(self):
        barbranch = BarBranch.objects.get(pk=1)
        field_label = barbranch._meta.get_field("latitude").verbose_name
        self.assertEquals(field_label, "Latitude")

    def test_model_barbranch_longitude_label(self):
        barbranch = BarBranch.objects.get(pk=1)
        field_label = barbranch._meta.get_field("longitude").verbose_name
        self.assertEquals(field_label, "Longitude")

    def test_model_barbranch_address_max_length(self):
        barbranch = BarBranch.objects.get(pk=1)
        max_length = barbranch._meta.get_field("address").max_length
        self.assertEquals(max_length, 255)

    def test_model_barbranch_metro_max_length(self):
        barbranch = BarBranch.objects.get(pk=1)
        max_length = barbranch._meta.get_field("metro").max_length
        self.assertEquals(max_length, 255)

    def test_model_barbranch_object_name(self):
        barbranch = BarBranch.objects.get(pk=1)
        expected_object_name = "%s - %s" % (barbranch.bar.name, barbranch.metro)
        self.assertEquals(expected_object_name, str(barbranch))

    def test_model_barbranch_object_repr(self):
        barbranch = BarBranch.objects.get(pk=1)
        expected_object_repr = "<BarBranch: %s - %s>" % (barbranch.bar.name, barbranch.metro)
        self.assertEquals(expected_object_repr, repr(barbranch))
