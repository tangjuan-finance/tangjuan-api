from app.service.simulations.base import BaseSimulationService
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from app.domain.entities import AssetDomain

from app.repository.entities import AssetRepo
from typing import Type


class AssetSimulationService(BaseSimulationService):
    VALID_STRATEGY = {
        "random_rate": RandomRateStrategy,
    }
    DEFAULT_STRATEGY = "random_rate"

    @classmethod
    def simulate_asset(cls, account_id: str, payload: dict) -> dict:
        asset_id, strategy_name = (
            payload.get("asset_id"),
            payload.get("strategy", cls.DEFAULT_STRATEGY),
        )

        # Get asset
        if not asset_id:
            raise ValueError("Asset ID is required")
        asset = cls._get_resource_domain_by_repo(
            account_id=account_id, entity_id=asset_id, repo=AssetRepo
        )

        # Get strategy
        strategy_class = cls._get_strategy_class(
            strategy=strategy_name, valid_strategies=cls.VALID_STRATEGY
        )
        strategy = cls._build_strategy_from_asset(
            strategy_class=strategy_class, asset=asset
        )

        return cls._generate_simulation(
            amount=asset.amount,
            start=asset.start_age,
            end=asset.end_age,
            strategy=strategy,
        )

    @classmethod
    def _build_strategy_from_asset(
        cls, strategy_class: Type[BaseSimulateStrategy], asset: AssetDomain
    ):
        if strategy_class == RandomRateStrategy:
            min_rate = getattr(asset, "min_yearly_return_rate")
            if min_rate is None:
                raise ValueError("min rate should be given.")
            max_rate = getattr(asset, "max_yearly_return_rate")
            if max_rate is None:
                raise ValueError("max rate should be given.")

            return RandomRateStrategy(min_rate=min_rate, max_rate=max_rate)

        raise ValueError(f"Unsupported strategy class: {strategy_class.__name__}")
