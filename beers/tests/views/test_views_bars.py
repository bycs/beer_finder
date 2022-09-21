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


def express_bar(bar: Bar) -> Dict[str, Any]:
    return {"id": bar.id, "name": bar.name, "website": bar.website}


express_bars = pluralized(express_bar)


@pytest.mark.django_db
class TestBarViewSet(ViewSetTest):
    list_url = lambda_fixture(lambda: url_for("bars-list"))

    detail_url = lambda_fixture(lambda bar: url_for("bars-detail", bar.pk))

    class TestList(UsesGetMethod, UsesListEndpoint, Returns200):
        bars = lambda_fixture(
            lambda: [
                Bar.objects.create(name=name, website=website)
                for name, website in (
                    ["Bar #1", "bar1.exemple"],
                    ["Cool Bar", "coolbar.exemple"],
                    ["Bar", "bar.exemple"],
                )
            ],
            autouse=True,
        )

        def test_it_returns_bars(self, bars, results):
            expected = express_bars(sorted(bars, key=lambda bar: bar.id))
            actual = sorted(results, key=lambda bar: bar["id"])
            assert expected == actual

    class TestCreate(UsesPostMethod, UsesListEndpoint, Returns405):
        data = static_fixture({"name": "Baaaaar", "website": "baaaaar.exemple"})

    class TestRetrieve(UsesGetMethod, UsesDetailEndpoint, Returns200):
        bar = lambda_fixture(lambda: Bar.objects.create(name="Baaaaar", website="baaaaar.exemple"))

        def test_it_returns_bar(self, bar, json):
            expected = express_bar(bar)
            actual = json
            assert expected == actual

    class TestUpdate(UsesPatchMethod, UsesDetailEndpoint, Returns405):
        bar = lambda_fixture(lambda: Bar.objects.create(name="Bar #1", website="baaaaar.com"))

    class TestDestroy(UsesDeleteMethod, UsesDetailEndpoint, Returns405):
        bar = lambda_fixture(lambda: Bar.objects.create(name="Baaaaar", website="baaaaar.exemple"))
