from app.service.simulations.base import BaseAssociationSimulationService
from .config import ScenarioIncomeSimulationConfig


class ScenarioIncomeSimulationService(BaseAssociationSimulationService):
    @classmethod
    def simulate_income_in_scenario(cls, account_id: str, payload: dict) -> dict:
        service = BaseAssociationSimulationService(ScenarioIncomeSimulationConfig)
        return service.simulate_resource_in_scenario(
            account_id=account_id, payload=payload
        )

    @classmethod
    def simulate_incomes_in_scenario(cls, account_id: str, payload: dict) -> dict:
        service = BaseAssociationSimulationService(ScenarioIncomeSimulationConfig)
        return service.simulate_resources_in_scenario(
            account_id=account_id, payload=payload
        )

    @classmethod
    def aggregate_incomes_in_scenario(cls, account_id: str, payload: dict) -> dict:
        service = BaseAssociationSimulationService(ScenarioIncomeSimulationConfig)
        return service.aggregate_simulations_by_age(
            account_id=account_id, payload=payload
        )
