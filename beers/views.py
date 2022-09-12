from collections import Counter

from beers.decorators import staff_required
from beers.logics import sync_to_db
from beers.models.bars import Bar, BarBranch
from beers.models.beers import Beer
from beers.serializers import BarBranchSerializer, BarSerializer, BeerSerializer

from django.db.models import Func
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response


@staff_required
def sync_all_beers(request):
    sync_to_db.sync_lambic()
    sync_to_db.sync_we_cidreria()
    sync_to_db.sync_we_pub()
    return HttpResponse("Все ок!")


@api_view(["GET"])
def filter_beers(request, bar_id: int | None = None, **kwargs: list[dict[str, str]]):
    if bar_id is None:
        beers = Beer.objects.all()
    else:
        beers = Beer.objects.filter(bar_id=bar_id)
    if kwargs:
        for key, value in kwargs.items():
            beers = beers.filter(specifications__contains={key: value})
    serializer = BeerSerializer(beers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def top_spec_beers_v1(request):
    queryset = Beer.objects.all().values("specifications")
    specifications = [item["specifications"] for item in queryset]
    keys = set()
    keys_list = []
    key_count = {}

    for spec in specifications:
        keys.update(spec.keys())
        keys_list += list(spec.keys())
    for key in keys:
        key_count[key] = keys_list.count(key)

    key_count = dict(sorted(key_count.items(), key=lambda item: item[1], reverse=True))
    top_keys = list(key_count.keys())[:7]
    return Response(data=top_keys)


@api_view(["GET"])
def top_spec_beers_v2(request):
    class JsonKeys(Func):
        function = "jsonb_object_keys"

    json_keys = Beer.objects.all().annotate(metadata_keys=JsonKeys("specifications"))
    json_keys = json_keys.values_list("metadata_keys", flat=True)
    top_keys = dict(Counter(json_keys))
    sorted_keys = dict(sorted(top_keys.items(), key=lambda x: x[1], reverse=True))
    return Response(data=sorted_keys)


class BeersViewSet(viewsets.ModelViewSet):
    queryset = Beer.objects.all().order_by("name")
    serializer_class = BeerSerializer
    http_method_names = ("get",)


class BarsViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all().order_by("name")
    serializer_class = BarSerializer
    http_method_names = ("get",)


class BarBranchesViewSet(viewsets.ModelViewSet):
    queryset = BarBranch.objects.all().order_by("bar__name")
    serializer_class = BarBranchSerializer
    http_method_names = ("get",)
