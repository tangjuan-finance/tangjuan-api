from app.repository.entities import ScenarioRepo
from app.service.mixin import CheckOwnershipMixin


class BaseAssociationService(CheckOwnershipMixin):
    """Base for all associations"""

    @classmethod
    def _check_scenario_ownership(cls, account_id: str, scenario_id: str) -> str:
        if not isinstance(scenario_id, str):
            raise TypeError(
                f"Scenario ID should be type str, not type {type(scenario_id).__name__}"
            )

        scenario_from_repo = ScenarioRepo.get_by_id(scenario_id=scenario_id)

        if not scenario_from_repo:
            raise ValueError(f"Scenario with ID {scenario_id} not found")

        cls._check_ownership_by_id(
            account_id=account_id, owner_id=scenario_from_repo.owner.id
        )

        return "This account owned this scenario"
