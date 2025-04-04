# from decimal import Decimal
from tests.factory import AssetDomainFactory
from app.domain.simulations.strategies.random_rate_strategy import RandomRateStrategy


class TestRandomRateStrategyCase:
    def test_create_simulate(self):
        asset = AssetDomainFactory()
        # asset.end_age =
        value, start_age, end_age, min_rate, max_rate = (
            asset.amount,
            asset.start_age,
            asset.end_age,
            asset.min_rate,
            asset.max_rate,
        )
        result = RandomRateStrategy.apply(
            value=value,
            start_age=start_age,
            end_age=end_age,
            min_rate=min_rate,
            max_rate=max_rate,
        )
        ages, values = result.get("ages"), result.get("values")

        # Assert: Check if both ages and values existed
        assert ages is not None
        assert values is not None

        # Assert: Check if both ages and values are a list
        assert isinstance(ages, list)
        assert isinstance(values, list)
