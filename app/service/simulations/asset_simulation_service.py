from .base import BaseSimulationService
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from app.domain.entities import AssetDomain
from app.repository.entities import AssetRepo
from decimal import Decimal, ROUND_UP


class AssetSimulationService(BaseSimulationService):
    VALID_STRATEGY = {
        "random_rate": RandomRateStrategy,
    }

    @classmethod
    def _get_asset_entity(cls, account_id: str, payload: dict) -> AssetDomain:
        asset_id = payload.get("asset_id")
        if not asset_id:
            raise ValueError("Asset ID is required")

        asset_from_repo = AssetRepo.get_by_id(asset_id=asset_id)
        if not asset_from_repo:
            raise ValueError(f"Asset with ID {asset_id} not found")

        # Check if the account own the asset
        cls._check_ownership_by_id(
            account_id=account_id, owner_id=asset_from_repo.owner.id
        )
        return asset_from_repo

    @classmethod
    def _get_strategy(cls, payload: dict) -> BaseSimulateStrategy:
        strategy = payload.get("strategy")

        # Default Strategy: RandomRateStrategy
        if not strategy:
            return RandomRateStrategy

        # If strategy is given, check if the given strategy is valid
        strategy_class = cls.VALID_STRATEGY.get(str(strategy))
        if not strategy_class:
            raise ValueError(f"Invalid strategy {strategy}")

        return strategy_class

    @classmethod
    def _simulate(cls, asset: AssetDomain, strategy_class: BaseSimulateStrategy):
        if strategy_class == RandomRateStrategy:
            return cls._simulate_by_random_rate(asset=asset)
        else:
            raise ValueError(f"Invalid Strategy {strategy_class.__name__}")

    @classmethod
    def _simulate_by_random_rate(cls, asset: AssetDomain) -> list:
        value, start_age, end_age, min_rate, max_rate = (
            asset.amount,
            asset.start_age,
            asset.end_age,
            asset.min_yearly_return_rate,
            asset.max_yearly_return_rate,
        )

        prev = Decimal(value).quantize(exp=Decimal("1.00"), rounding=ROUND_UP)
        values = [prev]

        for _ in range(start_age + 1, end_age + 1):
            prev = RandomRateStrategy.apply(
                value=prev,
                min_rate=min_rate,
                max_rate=max_rate,
            )
            values.append(prev)

        return values

    @classmethod
    def simulate_asset(cls, account_id: str, payload: dict) -> dict:
        asset = cls._get_asset_entity(account_id=account_id, payload=payload)
        strategy_class = cls._get_strategy(payload)
        return {
            "ages": cls._get_duration(start=asset.start_age, end=asset.end_age),
            "values": cls._simulate(asset=asset, strategy_class=strategy_class),
        }
