from collections import Counter
from operator import itemgetter

from django.db.models import QuerySet

from beers.managers.beers import JsonKeys
from beers.models.bars import Bar
from beers.models.beers import Beer


def get_bars() -> list:
    bars: QuerySet = Bar.objects.all().values_list("name", flat=True)
    return list(bars)


def get_top_keys(bar: str | None = None) -> list:
    if bar:
        beers = Beer.objects.filter(bar__name=bar)
    else:
        beers = Beer.objects.all()
    json_keys = beers.annotate(metadata_keys=JsonKeys("specifications"))
    json_keys = json_keys.values_list("metadata_keys", flat=True)
    top_keys = dict(Counter(json_keys))
    sorted_keys = dict(sorted(top_keys.items(), key=lambda x: x[1], reverse=True)[:7])
    result = sorted_keys.keys()
    return [result for result in result if result]


def get_top_values(bar: str | None = None, key: str | None = None) -> list:
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
    result = values_sorted.keys()
    return [result for result in result if result]


def filter_beers(bar: str | None = None, *args: dict[str, str]) -> list[Beer]:
    result: list[Beer] = []
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

    result += beers
    return result
