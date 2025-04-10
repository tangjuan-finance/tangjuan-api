from app.service.simulations.base import BaseSimulationService
from .config import AssetSimulationConfig


class AssetSimulationService(BaseSimulationService):
    @classmethod
    def simulate_asset(cls, account_id: str, payload: dict) -> dict:
        service = BaseSimulationService(config=AssetSimulationConfig)
        return service.simulate_entity(account_id=account_id, payload=payload)
        # asset_id, strategy_name = cls.validate_simulation_input(
        #     payload=payload,
        #     resource_type=cls.RESOURCE_TYPE,
        #     default_strategy=cls.DEFAULT_STRATEGY,
        # )

        # # Get asset
        # asset = cls._get_resource_domain_by_repo(entity_id=asset_id, repo=AssetRepo)
        # # Check if the account own the asset
        # cls._check_entity_ownership(account_id=account_id, entity=asset)

        # # Get strategy
        # strategy = cls._build_strategy_from_entity(
        #     strategy_name=strategy_name, entity=asset
        # )

        # return cls._generate_simulation(
        #     amount=asset.amount,
        #     start=asset.start_age,
        #     end=asset.end_age,
        #     strategy=strategy,
        # )
