from .base import BaseSimulationService
# from app.domain.simulations.strategies import RandomRateStrategy


class AssetSimulationService(BaseSimulationService):
    @classmethod
    # def sim(cls):
    #     cls._
    #        house_id = payload.get("id")
    #     if not house_id:
    #         raise ValueError("House ID is required")
    #     house_from_repo = HouseRepo.get_by_id(house_id)

    #     if not house_from_repo:
    #         raise ValueError(f"House with ID {house_id} not found")

    #     # Check if the account owns the house
    #     if house_from_repo.owner.id != account_id:
    #         raise PermissionError(f"Account {account_id} does not own this resource")

    @classmethod
    def simulate_asset(cls, account_id: str, payload: dict) -> dict:
        # asset_id: str, strategy: str = "random_rate"
        return {
            "ages": [1, 2, 3],
            "values": [10, 20, 30],
        }
