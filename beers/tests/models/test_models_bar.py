from datetime import datetime

from django.test import TestCase

from beers.models.bars import Bar


class BarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        bar = Bar.objects.create(name="Cool Bar", website="https://cool-bar.com")
        cls.bar = bar

    def test_model_bar_it_has_fields(self) -> None:
        self.assertIsInstance(self.bar.name, str)
        self.assertIsInstance(self.bar.website, str)
        self.assertIsInstance(self.bar.updated, datetime | None)

    def test_model_bar_name_label(self) -> None:
        bar = Bar.objects.get(pk=1)
        field_label = bar._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Name")

    def test_model_bar_website_label(self) -> None:
        bar = Bar.objects.get(pk=1)
        field_label = bar._meta.get_field("website").verbose_name
        self.assertEqual(field_label, "Website")

    def test_model_bar_updated_label(self) -> None:
        bar = Bar.objects.get(pk=1)
        field_label = bar._meta.get_field("updated").verbose_name
        self.assertEqual(field_label, "Updated")

    def test_model_bar_name_max_length(self) -> None:
        bar = Bar.objects.get(pk=1)
        max_length = bar._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_model_bar_object_name(self) -> None:
        bar = Bar.objects.get(pk=1)
        expected_object_name = "%s" % (bar.name)
        self.assertEqual(expected_object_name, str(bar))

    def test_model_bar_object_repr(self) -> None:
        bar = Bar.objects.get(pk=1)
        expected_object_name = "<Bar: %s>" % (bar.name)
        self.assertEqual(expected_object_name, repr(bar))
