# Generated by Django 4.1.1 on 2022-09-20 09:37

import django.db.models.deletion

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("beers", "0006_barbranch_latitude"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bar",
            options={"ordering": ("name",), "verbose_name": "Bar", "verbose_name_plural": "Bars"},
        ),
        migrations.AlterModelOptions(
            name="barbranch",
            options={
                "ordering": ("bar", "metro"),
                "verbose_name": "BarBranch",
                "verbose_name_plural": "BarBranches",
            },
        ),
        migrations.AlterModelOptions(
            name="beer",
            options={
                "ordering": ("name", "bar"),
                "verbose_name": "Beer",
                "verbose_name_plural": "Beers",
            },
        ),
        migrations.AlterField(
            model_name="bar",
            name="name",
            field=models.CharField(max_length=255, unique=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="bar",
            name="updated",
            field=models.DateTimeField(default=None, null=True, verbose_name="Updated"),
        ),
        migrations.AlterField(
            model_name="bar",
            name="website",
            field=models.URLField(unique=True, verbose_name="Website"),
        ),
        migrations.AlterField(
            model_name="barbranch",
            name="address",
            field=models.CharField(max_length=255, unique=True, verbose_name="Address"),
        ),
        migrations.AlterField(
            model_name="barbranch",
            name="bar",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="beers.bar", verbose_name="Bar"
            ),
        ),
        migrations.AlterField(
            model_name="barbranch",
            name="latitude",
            field=models.FloatField(default=None, null=True, verbose_name="Latitude"),
        ),
        migrations.AlterField(
            model_name="barbranch",
            name="longitude",
            field=models.FloatField(default=None, null=True, verbose_name="Longitude"),
        ),
        migrations.AlterField(
            model_name="barbranch",
            name="metro",
            field=models.CharField(max_length=255, verbose_name="Metro"),
        ),
        migrations.AlterField(
            model_name="beer",
            name="bar",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="beers.bar", verbose_name="Bar"
            ),
        ),
        migrations.AlterField(
            model_name="beer",
            name="description",
            field=models.TextField(default=None, null=True, verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="beer",
            name="name",
            field=models.CharField(max_length=255, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="beer",
            name="price",
            field=models.IntegerField(default=None, null=True, verbose_name="Price"),
        ),
        migrations.AlterField(
            model_name="beer",
            name="specifications",
            field=models.JSONField(default=dict, null=True, verbose_name="Specifications"),
        ),
    ]