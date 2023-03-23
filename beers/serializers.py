from rest_framework import serializers

from beers.models.bars import Bar
from beers.models.bars import BarBranch
from beers.models.beers import Beer


class BeerSerializer(serializers.HyperlinkedModelSerializer):
    bar = serializers.CharField(source="bar.name", read_only=True)

    class Meta:
        model = Beer
        fields = "__all__"


class BarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bar
        exclude = ("updated",)


class BarBranchSerializer(serializers.HyperlinkedModelSerializer):
    bar = serializers.CharField(source="bar.name", read_only=True)

    class Meta:
        model = BarBranch
        fields = "__all__"
