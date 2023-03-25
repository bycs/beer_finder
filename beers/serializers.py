from rest_framework import serializers

from beers.models.bars import Bar
from beers.models.bars import BarBranch
from beers.models.beers import Beer


class BeerSerializer(serializers.HyperlinkedModelSerializer):
    bar_pk = serializers.CharField(source="bar.pk", read_only=True)
    bar_name = serializers.CharField(source="bar.name", read_only=True)

    class Meta:
        model = Beer
        fields = ["pk", "name", "price", "description", "specifications", "bar_name", "bar_pk"]


class BarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bar
        fields = ["pk", "name", "website"]


class BarBranchSerializer(serializers.HyperlinkedModelSerializer):
    bar_pk = serializers.CharField(source="bar.pk", read_only=True)
    bar_name = serializers.CharField(source="bar.name", read_only=True)

    class Meta:
        model = BarBranch
        fields = ["pk", "address", "metro", "bar_name", "bar_pk", "latitude", "longitude"]
