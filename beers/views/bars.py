from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from beers.models.bars import Bar
from beers.models.bars import BarBranch
from beers.serializers import BarBranchSerializer
from beers.serializers import BarSerializer


class BarsViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    http_method_names = ["get"]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = {
        "name": ["contains"],
        "website": ["contains"],
    }


class BarBranchesViewSet(viewsets.ModelViewSet):
    queryset = BarBranch.objects.all()
    serializer_class = BarBranchSerializer
    http_method_names = ["get"]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = {
        "bar__uuid": ["in"],
        "bar__name": ["in"],
        "address": ["contains"],
        "metro": ["in"],
    }
