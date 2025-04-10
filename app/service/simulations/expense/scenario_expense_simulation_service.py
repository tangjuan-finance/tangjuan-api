from app.service.simulations.base import BaseAssociationSimulationService
from .config import ScenarioExpenseSimulationConfig


class ScenarioExpenseSimulationService(BaseAssociationSimulationService):
    @classmethod
    def simulate_expense_in_scenario(cls, account_id: str, payload: dict) -> dict:
        service = BaseAssociationSimulationService(ScenarioExpenseSimulationConfig)
        return service.simulate_resource_in_scenario(
            account_id=account_id, payload=payload
        )

    @classmethod
    def simulate_expenses_in_scenario(cls, account_id: str, payload: dict) -> dict:
        service = BaseAssociationSimulationService(ScenarioExpenseSimulationConfig)
        return service.simulate_resources_in_scenario(
            account_id=account_id, payload=payload
        )

    @classmethod
    def aggregate_expenses_in_scenario(cls, account_id: str, payload: dict) -> dict:
        service = BaseAssociationSimulationService(ScenarioExpenseSimulationConfig)
        return service.aggregate_simulations_by_age(
            account_id=account_id, payload=payload
        )
