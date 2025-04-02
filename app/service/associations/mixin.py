from app.repository.entities import ScenarioRepo


class BaseAssociationService:
    """Mixin for all associations"""

    @staticmethod
    def _check_scenario_ownership(account_id: str, scenario_id: str) -> str:
        scenario_from_repo = ScenarioRepo.get_by_id(scenario_id=scenario_id)

        if not scenario_from_repo:
            raise ValueError(f"Scenario with ID {scenario_id} not found")

        if scenario_from_repo.owner.id != account_id:
            raise PermissionError(f"Account {account_id} does not own this scenario")

        return "This account owned this scenario"
