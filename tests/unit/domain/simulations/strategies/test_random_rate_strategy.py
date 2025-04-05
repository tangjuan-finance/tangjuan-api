from app.domain.entities import AssetDomain
from app.domain.simulations.strategies.random_rate_strategy import RandomRateStrategy


class TestRandomRateStrategyCase:
    @staticmethod
    def _generate_asset_simulate(asset: AssetDomain) -> dict:
        return RandomRateStrategy.apply(
            value=asset.amount,
            start_age=asset.start_age,
            end_age=asset.end_age,
            min_rate=asset.min_yearly_return_rate,
            max_rate=asset.max_yearly_return_rate,
        )

    def test_check_simulate_result_type(self, default_asset_domain):
        result = self._generate_asset_simulate(default_asset_domain)
        ages, values = result.get("ages"), result.get("values")

        # Assert: Check if both ages and values existed
        assert ages is not None
        assert values is not None

        # Assert: Check if both ages and values are a list
        assert isinstance(ages, list)
        assert isinstance(values, list)

    def test_check_simulate_result_boundry(self, default_asset_domain):
        result = self._generate_asset_simulate(default_asset_domain)
        ages, values = result.get("ages"), result.get("values")

        # Assert: Check if ages in bound
        assert ages is not None
        assert values is not None

        # Assert: Check if both ages and values are a list
        assert isinstance(ages, list)
        assert isinstance(values, list)

        # Arrange: Get rate interval
        min_rate, max_rate = (
            default_asset_domain.min_yearly_return_rate,
            default_asset_domain.max_yearly_return_rate,
        )

        # Arange: Create min boundry
        default_asset_domain.max_yearly_return_rate = min_rate
        min_values = self._generate_asset_simulate(default_asset_domain)["values"]

        # Arange: Create max boundry
        default_asset_domain.min_yearly_return_rate = (
            default_asset_domain.max_yearly_return_rate
        ) = max_rate
        max_values = self._generate_asset_simulate(default_asset_domain)["values"]

        for idx in range(len(values)):
            assert min_values[idx] <= values[idx] <= max_values[idx]
