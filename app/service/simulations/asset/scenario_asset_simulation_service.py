from app.service.simulations.asset import AssetSimulationService
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from app.domain.entities import AssetDomain

# from app.domain.associations import ScenarioAssetDomain
from app.repository.entities import AssetRepo
from decimal import Decimal, ROUND_UP
from typing import Type  # ,Optional


class ScenarioAssetSimulationService(AssetSimulationService):
    @classmethod
    def simulate_asset_in_scenario(cls, account_id: str, payload: dict) -> dict:
        asset = cls._get_asset_entity(account_id=account_id, payload=payload)
        # assoc = cls._get_assoc_entity(account_id=account_id, payload=payload)
        strategy_class = cls._get_strategy_class(payload)
        strategy = cls._build_strategy_from_asset(
            strategy_class=strategy_class, asset=asset
        )

        return {
            "ages": cls._get_duration(start=asset.start_age, end=asset.end_age),
            "values": cls._simulate(
                amount=asset.amount,
                start=asset.start_age,
                end=asset.end_age,
                strategy=strategy,
            ),
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
    def _get_strategy_class(cls, payload: dict) -> Type[BaseSimulateStrategy]:
        # Default Strategy: random_rate
        strategy = payload.get("strategy", "random_rate")

        # If strategy is given, check if the given strategy is valid
        strategy_class = cls.VALID_STRATEGY.get(str(strategy))
        if not strategy_class:
            raise ValueError(f"Invalid strategy {strategy}")

        return strategy_class

    @classmethod
    def _build_strategy_from_asset(
        cls, strategy_class: Type[BaseSimulateStrategy], asset: AssetDomain
    ):
        if strategy_class == RandomRateStrategy:
            min_rate = getattr(asset, "min_yearly_return_rate")
            if not min_rate:
                raise ValueError("min rate should be given.")
            max_rate = getattr(asset, "max_yearly_return_rate")
            if not max_rate:
                raise ValueError("max rate should be given.")

            return RandomRateStrategy(min_rate=min_rate, max_rate=max_rate)

        raise ValueError(f"Unsupported strategy class: {strategy_class.__name__}")

    @classmethod
    def _simulate(
        cls, amount: int, start: int, end: int, strategy: BaseSimulateStrategy
    ) -> list:
        prev = Decimal(amount).quantize(exp=Decimal("1.00"), rounding=ROUND_UP)
        values = [prev]

        for _ in range(start + 1, end + 1):
            prev = strategy.apply(prev)
            values.append(prev)
        return values
