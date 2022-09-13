from collections import Counter

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response

from beers.decorators import staff_required
from beers.logics import sync_to_db
from beers.managers.beers import JsonKeys
from beers.models.bars import Bar
from beers.models.bars import BarBranch
from beers.models.beers import Beer
from beers.serializers import BarBranchSerializer
from beers.serializers import BarSerializer
from beers.serializers import BeerSerializer


@staff_required
def sync_all_beers(request) -> HttpResponse:
    sync_to_db.sync_lambic()
    sync_to_db.sync_we_cidreria()
    sync_to_db.sync_we_pub()
    return HttpResponse("Все ок!")


class FilterBeersViewSet(viewsets.ViewSet):
    def list(self, request, bar_id: int | None = None, **kwargs: list[dict[str, str]]) -> Response:
        if bar_id is None:
            beers = Beer.objects.all()
        else:
            beers = Beer.objects.filter(bar_id=bar_id)
        if kwargs:
            for key, value in kwargs.items():
                beers = beers.filter(specifications__contains={key: value})
        serializer = BeerSerializer(beers, many=True)
        return Response(serializer.data)


class TopSpecV1ViewSet(viewsets.ViewSet):
    def list(self, request) -> Response:
        queryset = Beer.objects.all().values("specifications")
        specifications = [item["specifications"] for item in queryset]
        keys = set()
        keys_list = []
        key_count = {}

        for spec in specifications:
            if spec:
                keys.update(spec.keys())
                keys_list += list(spec.keys())
        for key in keys:
            key_count[key] = keys_list.count(key)

        key_count = dict(sorted(key_count.items(), key=lambda item: item[1], reverse=True))
        top_keys = list(key_count.keys())[:7]
        return Response(data=top_keys)


class TopSpecV2ViewSet(viewsets.ViewSet):
    def list(self, request) -> Response:
        json_keys = Beer.objects.all().annotate(metadata_keys=JsonKeys("specifications"))
        json_keys = json_keys.values_list("metadata_keys", flat=True)
        top_keys = dict(Counter(json_keys))
        sorted_keys = dict(sorted(top_keys.items(), key=lambda x: x[1], reverse=True)[:7])
        return Response(data=sorted_keys.keys())


class BeersViewSet(viewsets.ModelViewSet):
    queryset = Beer.objects.all().order_by("name")
    serializer_class = BeerSerializer
    http_method_names = ["get"]


class BarsViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all().order_by("name")
    serializer_class = BarSerializer
    http_method_names = ["get"]


class BarBranchesViewSet(viewsets.ModelViewSet):
    queryset = BarBranch.objects.all().order_by("bar__name")
    serializer_class = BarBranchSerializer
    http_method_names = ["get"]
