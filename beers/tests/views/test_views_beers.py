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
from beers.models.beers import Beer


def express_beer(beer: Beer) -> Dict[str, Any]:
    return {
        "id": beer.id,
        "name": beer.name,
        "price": beer.price,
        "description": beer.description,
        "specifications": beer.specifications,
        "bar": beer.bar.name,
    }


express_beers = pluralized(express_beer)


@pytest.mark.django_db
class TestBeerViewSet(ViewSetTest):
    list_url = lambda_fixture(lambda: url_for("beers-list"))

    detail_url = lambda_fixture(lambda beer: url_for("beers-detail", beer.pk))

    class TestList(UsesGetMethod, UsesListEndpoint, Returns200):
        beers = lambda_fixture(
            lambda: [
                Beer.objects.create(
                    bar=Bar.objects.get_or_create(name="Bar #1", defaults={"website": "b1.com"})[0],
                    name=name,
                    price=price,
                    description=description,
                    specifications=specifications,
                )
                for name, price, description, specifications in (
                    [
                        "Beer #1",
                        100000,
                        'Cool beer #1 with "quotes" and "new',
                        None,
                    ],
                    [
                        "Beer #2",
                        None,
                        "Soft beer #2",
                        {"alcohol": 5.0, "volume": 0.5},
                    ],
                    [
                        "Beer #1",
                        100000,
                        None,
                        {"alcohol": 2.0, "volume": 0.52},
                    ],
                )
            ],
            autouse=True,
        )

        def test_it_returns_beers(self, beers, results):
            expected = express_beers(sorted(beers, key=lambda beer: beer.id))
            actual = sorted(results, key=lambda beer: beer["id"])
            assert expected == actual

    class TestCreate(UsesPostMethod, UsesListEndpoint, Returns405):
        data = static_fixture(
            {
                "bar": "Bar #1",
                "name": "Free Beer",
                "price": 1,
                "description": "Free beer for everyone",
                "specifications": '{"alcohol": 3.2, "volume": 0.33}',
            }
        )

    class TestRetrieve(UsesGetMethod, UsesDetailEndpoint, Returns200):
        beer = lambda_fixture(
            lambda: Beer.objects.create(
                bar=Bar.objects.get_or_create(name="Bar #1", defaults={"website": "bar1.com"})[0],
                name="Expensive Beer",
                price=77777777,
                description=None,
                specifications=None,
            )
        )

        def test_it_returns_beer(self, beer, json):

            expected = express_beer(beer)
            actual = json
            assert expected == actual

    class TestUpdate(UsesPatchMethod, UsesDetailEndpoint, Returns405):
        beer = lambda_fixture(
            lambda: Beer.objects.create(
                bar=Bar.objects.get_or_create(name="Bar #1", defaults={"website": "bar1.com"})[0],
                name="Expensive Beer",
                price=77777777,
                description=None,
                specifications=None,
            )
        )

    class TestDestroy(UsesDeleteMethod, UsesDetailEndpoint, Returns405):
        beer = lambda_fixture(
            lambda: Beer.objects.create(
                bar=Bar.objects.get_or_create(name="Bar #1", defaults={"website": "bar1.com"})[0],
                name="Expensive Beer",
                price=77777777,
                description=None,
                specifications=None,
            )
        )
