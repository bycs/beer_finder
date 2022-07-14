from beers.models.beers import Beer

from rest_framework import serializers


class BeerSerializer(serializers.HyperlinkedModelSerializer):
    bar = serializers.CharField(source="bar.name", read_only=True)

    class Meta:
        model = Beer
        fields = ("name", "price", "description", "specifications", "bar")
        http_method_names = ("get",)
