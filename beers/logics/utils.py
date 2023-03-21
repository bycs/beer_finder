from django.db.models import Count
from django.db.models.query import QuerySet

from beers.managers.beers import JsonKeys
from beers.models.bars import BarBranch
from beers.models.beers import Beer


def get_bar_branches(bar: str | None = None) -> QuerySet:
    bar_branch = BarBranch.objects.select_related("bar").all().distinct()
    if bar:
        bar_branch = bar_branch.filter(bar__name=bar)
    return bar_branch


def get_top_keys(count: int = 6, bar: str | None = None) -> QuerySet:
    beers = Beer.objects.all()
    if bar:
        beers = beers.filter(bar__name=bar)
    json_keys = beers.annotate(json_keys=JsonKeys("specifications")).values("json_keys")
    top_keys = json_keys.annotate(count=Count("pk")).order_by("-count")[:count]
    top_keys = top_keys.values_list("json_keys", flat=True)
    return top_keys


def get_top_values(key: str, count: int = 6, bar: str | None = None) -> QuerySet:
    full_key = f"specifications__{key}"
    beers = Beer.objects.all()
    if bar:
        beers = beers.filter(bar__name=bar)
    filter_non_null = {f"{full_key}__isnull": False}
    values = beers.values(full_key).annotate(count=Count("pk")).filter(**filter_non_null)
    top_values = values.order_by("-count")[:count].values_list(full_key, flat=True)
    return top_values  # type: ignore[no-any-return]


def filter_beers(bar: str | None = None, count: int = 5, *args: dict) -> QuerySet[Beer]:
    beers = Beer.objects.select_related("bar").all().distinct()
    if bar:
        beers = beers.filter(bar__name=bar)

    if args:
        for arg in args:
            arg_key = list(arg.keys())[0]
            arg_value = list(arg.values())[0]
            if arg_key and arg_value:
                beers = beers.filter(specifications__contains=arg)
    beers = beers.order_by("?")[:count]
    return beers
