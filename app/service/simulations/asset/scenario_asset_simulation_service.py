from app.service.simulations.base import BaseAssociationSimulationService
from .config import ScenarioAssetSimulationConfig


class ScenarioAssetSimulationService(BaseAssociationSimulationService):
    @classmethod
    def simulate_asset_in_scenario(cls, account_id: str, payload: dict) -> dict:
        service = BaseAssociationSimulationService(ScenarioAssetSimulationConfig)
        return service.simulate_resource_in_scenario(
            account_id=account_id, payload=payload
        )

    @classmethod
    def simulate_assets_in_scenario(cls, account_id: str, payload: dict) -> dict:
        service = BaseAssociationSimulationService(ScenarioAssetSimulationConfig)
        return service.simulate_resources_in_scenario(
            account_id=account_id, payload=payload
        )

    @classmethod
    def aggregate_assets_in_scenario(cls, account_id: str, payload: dict) -> dict:
        service = BaseAssociationSimulationService(ScenarioAssetSimulationConfig)
        return service.aggregate_simulations_by_age(
            account_id=account_id, payload=payload
        )
