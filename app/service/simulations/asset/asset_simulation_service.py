from app.service.simulations.base import BaseSimulationService
from app.domain.simulations.strategies import RandomRateStrategy
from app.domain.entities import AssetDomain
from app.repository.entities import AssetRepo
from .base import BaseAssetSimulation


class AssetSimulationService(BaseSimulationService, BaseAssetSimulation):
    @classmethod
    def simulate_asset(cls, account_id: str, payload: dict) -> dict:
        asset_id, strategy_name = cls.validate_simulation_input(
            payload=payload,
            resource_type="asset",
            default_strategy=cls.DEFAULT_STRATEGY,
        )

        # Get asset
        asset = cls._get_resource_domain_by_repo(
            account_id=account_id, entity_id=asset_id, repo=AssetRepo
        )

        # Get strategy
        strategy = cls._build_strategy_from_asset(
            strategy_name=strategy_name, asset=asset
        )

        return cls._generate_simulation(
            amount=asset.amount,
            start=asset.start_age,
            end=asset.end_age,
            strategy=strategy,
        )

    @classmethod
    def _build_strategy_from_asset(cls, strategy_name: str, asset: AssetDomain):
        strategy_class = cls._get_strategy_class(
            strategy=strategy_name, valid_strategies=cls.VALID_STRATEGY
        )

        if strategy_class == RandomRateStrategy:
            min_rate = getattr(asset, "min_yearly_return_rate")
            if min_rate is None:
                raise ValueError("min rate should be given.")
            max_rate = getattr(asset, "max_yearly_return_rate")
            if max_rate is None:
                raise ValueError("max rate should be given.")

            return RandomRateStrategy(min_rate=min_rate, max_rate=max_rate)

        raise ValueError(f"Unsupported strategy class: {strategy_class.__name__}")
