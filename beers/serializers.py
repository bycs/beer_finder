from beers.models.bars import Bar, BarBranch
from beers.models.beers import Beer

from rest_framework import serializers


class BeerSerializer(serializers.HyperlinkedModelSerializer):
    bar = serializers.CharField(source="bar.name", read_only=True)

    class Meta:
        model = Beer
        fields = ("id", "name", "price", "description", "specifications", "bar")


class BarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bar
        fields = ("id", "name", "website")


class BarBranchSerializer(serializers.HyperlinkedModelSerializer):
    bar = serializers.CharField(source="bar.name", read_only=True)

    class Meta:
        model = BarBranch
        fields = ("id", "bar", "metro", "address")