from beers.models.bars import Bar, BarBranch
from beers.models.beers import Beer

from rest_framework import serializers


class BeerSerializer(serializers.HyperlinkedModelSerializer):
    bar = serializers.CharField(source="bar.name", read_only=True)

    class Meta:
        model = Beer
        fields = ("name", "price", "description", "specifications", "bar")
        http_method_names = ("get",)


class BarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bar
        fields = ("name", "website")
        http_method_names = ("get",)


class BarBranchSerializer(serializers.HyperlinkedModelSerializer):
    bar = serializers.CharField(source="bar.name", read_only=True)

    class Meta:
        model = BarBranch
        fields = ("bar", "metro", "address")
        http_method_names = ("get",)
