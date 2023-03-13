from typing import Any
from typing import Dict

import pytest

from pytest_drf import Returns200
from pytest_drf import Returns405
from pytest_drf import UsesDeleteMethod
from pytest_drf import UsesDetailEndpoint
from pytest_drf import UsesGetMethod
from pytest_drf import UsesListEndpoint
from pytest_drf import UsesPatchMethod
from pytest_drf import UsesPostMethod
from pytest_drf import ViewSetTest
from pytest_drf.util import pluralized
from pytest_drf.util import url_for
from pytest_lambda import lambda_fixture
from pytest_lambda import static_fixture

from beers.models.bars import Bar
from beers.models.bars import BarBranch


def express_barbranch(barbranch: BarBranch) -> Dict[str, Any]:
    return {
        "id": barbranch.id,
        "bar": barbranch.bar.name,
        "address": barbranch.address,
        "metro": barbranch.metro,
        "latitude": barbranch.latitude,
        "longitude": barbranch.longitude,
    }


express_barbranches = pluralized(express_barbranch)


@pytest.mark.django_db
class TestBarBranchViewSet(ViewSetTest):
    list_url = lambda_fixture(lambda: url_for("barbranches-list"))

    detail_url = lambda_fixture(lambda barbranch: url_for("barbranches-detail", barbranch.pk))

    class TestList(UsesGetMethod, UsesListEndpoint, Returns200):
        barbranches = lambda_fixture(
            lambda: [
                BarBranch.objects.create(
                    bar=Bar.objects.get_or_create(name="Bar #1", defaults={"website": "bar1.com"})[
                        0
                    ],
                    address=address,
                    metro=metro,
                    latitude=latitude,
                    longitude=longitude,
                )
                for address, metro, latitude, longitude in (
                    [
                        "Москва",
                        "Таганская",
                        55.742,
                        37.653,
                    ],
                    [
                        "Воронеж",
                        "Площадь Ленина",
                        51.667,
                        39.183,
                    ],
                    [
                        "Саратов",
                        "Курская",
                        None,
                        None,
                    ],
                )
            ],
            autouse=True,
        )

        def test_it_returns_barbranches(self, barbranches, results):
            expected = express_barbranches(sorted(barbranches, key=lambda barbranch: barbranch.id))
            actual = sorted(results, key=lambda barbranch: barbranch["id"])
            assert expected == actual

    class TestCreate(UsesPostMethod, UsesListEndpoint, Returns405):
        data = static_fixture(
            {
                "bar": "Bar #1",
                "address": "Москва",
                "metro": "Таганская",
                "latitude": 55.742,
                "longitude": 37.653,
            }
        )

    class TestRetrieve(UsesGetMethod, UsesDetailEndpoint, Returns200):
        barbranch = lambda_fixture(
            lambda: BarBranch.objects.create(
                bar=Bar.objects.get_or_create(name="Bar #1", defaults={"website": "bar1.com"})[0],
                address="Саратов",
                metro="Курская",
                latitude=None,
                longitude=None,
            )
        )

        def test_it_returns_barbranch(self, barbranch, json):
            expected = express_barbranch(barbranch)
            actual = json
            assert expected == actual

    class TestUpdate(UsesPatchMethod, UsesDetailEndpoint, Returns405):
        barbranch = lambda_fixture(
            lambda: BarBranch.objects.create(
                bar=Bar.objects.get_or_create(name="Bar #1", defaults={"website": "bar1.com"})[0],
                address="Саратов",
                metro="Курская",
                latitude=None,
                longitude=None,
            )
        )

    class TestDestroy(UsesDeleteMethod, UsesDetailEndpoint, Returns405):
        barbranch = lambda_fixture(
            lambda: BarBranch.objects.create(
                bar=Bar.objects.get_or_create(name="Bar #1", defaults={"website": "bar1.com"})[0],
                address="Саратов",
                metro="Курская",
                latitude=None,
                longitude=None,
            )
        )
