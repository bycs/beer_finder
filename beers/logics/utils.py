from collections import Counter
from operator import itemgetter

from django.db.models import QuerySet

from beers.managers.beers import JsonKeys
from beers.models.bars import Bar
from beers.models.bars import BarBranch
from beers.models.beers import Beer


def get_bars() -> QuerySet[Bar]:
    bars = Bar.objects.all()
    return bars


def get_bars_branches(bar: str | None = None) -> QuerySet[BarBranch]:
    if bar:
        bars_branch = BarBranch.objects.filter(bar__name=bar)
    else:
        bars_branch = BarBranch.objects.all()
    return bars_branch


def get_top_keys(bar: str | None = None) -> list[str]:
    if bar:
        beers = Beer.objects.filter(bar__name=bar)
    else:
        beers = Beer.objects.all()
    json_keys = beers.annotate(metadata_keys=JsonKeys("specifications"))
    keys = json_keys.values_list("metadata_keys", flat=True)
    keys_dict = dict(Counter(keys))
    sorted_tuple = sorted(keys_dict.items(), key=itemgetter(1), reverse=True)
    keys_sorted = dict(sorted_tuple[:7])
    result = list(keys_sorted.keys())
    return [x for x in result if x is not None]


def get_top_values(bar: str | None = None, key: str | None = None) -> list[str]:
    if bar:
        beers = Beer.objects.filter(bar__name=bar)
    else:
        beers = Beer.objects.all()

    if key:
        values = beers.values_list(f"specifications__{key}", flat=True)
    else:
        values = beers.values_list("specifications__", flat=True)

    values_dict = dict(Counter(values))
    sorted_tuple = sorted(values_dict.items(), key=itemgetter(1), reverse=True)
    values_sorted = dict(sorted_tuple[:7])
    result = list(values_sorted.keys())
    return [x for x in result if x is not None]


def filter_beers(bar: str | None = None, *args: dict[str, str | None]) -> QuerySet[Beer]:
    if bar is None:
        beers = Beer.objects.all()
    else:
        beers = Beer.objects.filter(bar__name=bar)

    if args:
        for arg in args:
            arg_key = list(arg.keys())[0]
            arg_value = list(arg.values())[0]
            if arg_key and arg_value:
                beers = beers.filter(specifications__contains=arg)

    return beers
