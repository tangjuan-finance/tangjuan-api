from app.domain.associations import ScenarioIncomeDomain
from app.repository.associations import ScenarioIncomeRepo
from app.repository.entities import IncomeRepo
from .mixin import BaseAssociationService


class ScenarioIncomeService(BaseAssociationService):
    @classmethod
    def create_scenario_income(cls, account_id: str, payload: dict) -> dict:
        """Create a new scenario income assoc with validated owner."""

        scenario_id, income_id = payload["scenario_id"], payload["income_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_income_ownership(account_id=account_id, income_id=income_id)

        # Create assoc based on payload
        assoc_domain = ScenarioIncomeDomain(**payload)
        assoc = ScenarioIncomeRepo.create(assoc_domain)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc)

    @classmethod
    def get_scenario_income_by_id(cls, account_id: str, payload: dict) -> dict:
        """Get the scenario income assoc by id with validated owner."""

        scenario_id, income_id = payload["scenario_id"], payload["income_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_income_ownership(account_id=account_id, income_id=income_id)

        # Get assoc by id
        assoc_from_repo = ScenarioIncomeRepo.get_by_id(
            scenario_id=scenario_id, income_id=income_id
        )

        if not assoc_from_repo:
            raise ValueError(
                f"Scenario Income Association with scenario ID {scenario_id} and income ID {income_id} not found"
            )

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc_from_repo)

    @classmethod
    def get_scenario_incomes(cls, account_id: str, payload: dict) -> list[dict]:
        """Get all scenario income assoc with validated owner."""

        scenario_id = payload["scenario_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)

        # Generate the list of dict based on the assocs got from the repo
        return [
            cls._create_response(assoc=assoc)
            for assoc in ScenarioIncomeRepo.get_list(scenario_id=scenario_id)
        ]

    @classmethod
    def update_scenario_income(cls, account_id: str, payload: dict) -> dict:
        """Update the scenario income assoc with validated owner."""

        # Get the Scenario Income Association
        assoc = cls.get_scenario_income_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Update the Scenario Income Association based on given payload
        for field in payload.keys():
            setattr(assoc, field, payload[field])

        # Set the change by repo
        updated_assoc = ScenarioIncomeRepo.save(assoc)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=updated_assoc)

    @classmethod
    def delete_scenario_income_by_id(cls, account_id: str, payload: dict) -> str:
        """Delete the scenario income assoc by ID with validated owner."""
        # Get the Scenario Income Association
        # Raises if not found or unauthorized
        cls.get_scenario_income_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Get the scenario and income ID
        scenario_id, income_id = payload["scenario_id"], payload["income_id"]

        # Delete the assoc
        ScenarioIncomeRepo.delete_by_id(scenario_id=scenario_id, income_id=income_id)

        return f"Scenario Income with scenario ID {scenario_id} and income ID {income_id} deleted successfully"

    @staticmethod
    def _create_response(assoc: ScenarioIncomeDomain) -> dict:
        return {
            "association": assoc,
            "income": IncomeRepo.get_by_id(income_id=assoc.income_id),
        }

    @staticmethod
    def _check_income_ownership(account_id: str, income_id: str) -> str:
        if not isinstance(income_id, str):
            raise TypeError(
                f"Income ID should be type str, not type {type(income_id).__name__}"
            )

        income_from_repo = IncomeRepo.get_by_id(income_id=income_id)

        if not income_from_repo:
            raise ValueError(f"Income with ID {income_id} not found")

        if income_from_repo.owner.id != account_id:
            raise PermissionError(f"Account {account_id} does not own this income")

        return "This account owned this income"
