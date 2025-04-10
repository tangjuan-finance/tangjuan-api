from app.service.simulations.base import BaseSimulationService
from .config import IncomeSimulationConfig


class IncomeSimulationService(BaseSimulationService):
    @classmethod
    def simulate_income(cls, account_id: str, payload: dict) -> dict:
        service = BaseSimulationService(config=IncomeSimulationConfig)
        return service.simulate_resource(account_id=account_id, payload=payload)
