from app.service.simulations import AssetSimulationService


class TestAssetSimulationServiceCase:
    """Test cases for AssetSimulationService."""

    def test_get_asset_simulation_by_id_service_type_checking(self, default_asset):
        """Test get the simulation of an asset by ID"""
        # Act: Get the simulation with default strategy
        result = AssetSimulationService.simulate(asset=default_asset)
        ages, values = result.get("ages"), result.get("values")

        # Assert: Check if both ages and values existed
        assert ages is not None
        assert values is not None

        # Assert: Check if both ages and values are a list
        assert isinstance(ages, list)
        assert isinstance(values, list)

    def test_get_asset_simulation_by_id_service_with_random_rate_strategy(
        self, default_asset
    ):
        """Test get the simulation of an asset by ID"""

        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arrange: Get rate interval
        min_rate, max_rate = (
            default_asset.min_yearly_return_rate,
            default_asset.max_yearly_return_rate,
        )

        # Act: Get the simulation
        _, values = AssetSimulationService.simulate(
            asset=default_asset, strategy=strategy
        )

        # Arange: Create min, max values boundry
        asset_with_min_rate = default_asset
        asset_with_min_rate.max_yearly_return_rate = min_rate

        asset_with_max_rate = default_asset
        asset_with_max_rate.min_yearly_return_rate = max_rate

        _, min_values = AssetSimulationService.simulate(
            asset=asset_with_min_rate, strategy=strategy
        )
        _, max_values = AssetSimulationService.simulate(
            asset=asset_with_max_rate, strategy=strategy
        )

        for idx in range(len(values)):
            assert min_values[idx] <= values[idx] <= max_values[idx]
