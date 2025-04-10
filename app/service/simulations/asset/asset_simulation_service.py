from app.service.simulations.base import BaseSimulationService
from .config import AssetSimulationConfig


class AssetSimulationService(BaseSimulationService):
    @classmethod
    def simulate_asset(cls, account_id: str, payload: dict) -> dict:
        service = BaseSimulationService(config=AssetSimulationConfig)
        return service.simulate_resource(account_id=account_id, payload=payload)
