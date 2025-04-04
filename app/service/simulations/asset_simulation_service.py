from .mixin import BaseSimulationService
from app.domain.entities import AssetDomain


class AssetSimulationService(BaseSimulationService):
    @classmethod
    def simulate(cls, asset: AssetDomain, strategy: str = "random_rate") -> dict:
        return {
            "ages": [1, 2, 3],
            "values": [10, 20, 30],
        }
