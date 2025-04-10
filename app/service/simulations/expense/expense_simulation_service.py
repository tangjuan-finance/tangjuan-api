from app.service.simulations.base import BaseSimulationService
from .config import ExpenseSimulationConfig


class ExpenseSimulationService(BaseSimulationService):
    @classmethod
    def simulate_expense(cls, account_id: str, payload: dict) -> dict:
        service = BaseSimulationService(config=ExpenseSimulationConfig)
        return service.simulate_resource(account_id=account_id, payload=payload)
