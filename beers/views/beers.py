from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from beers.logics.utils import get_top_keys
from beers.models.beers import Beer
from beers.serializers import BeerSerializer


class BeersViewSet(viewsets.ModelViewSet):
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    http_method_names = ["get"]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = {
        "bar__name": ["in"],
        "name": ["contains"],
        "price": ["gte", "lte"],
        "description": ["contains"],
    }


class TopSpecKeyViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        params = dict(request.query_params)
        bar__name = params.get("bar__name")
        keys = get_top_keys(count=10, bar=bar__name)
        return Response(data=keys)


class FilterBeersViewSet(viewsets.ViewSet):
    def list(
        self, request: Request, bar_id: int | None = None, **kwargs: tuple[dict[str, str]]
    ) -> Response:
        beers = Beer.objects.all()
        if bar_id:
            beers = Beer.objects.filter(bar_id=bar_id)
        if kwargs:
            for key, value in kwargs.items():
                beers = beers.filter(specifications__contains={key: value})
        serializer = BeerSerializer(beers, many=True)
        return Response(serializer.data)
