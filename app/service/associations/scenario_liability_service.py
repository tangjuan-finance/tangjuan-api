from app.domain.associations import ScenarioLiabilityDomain
from app.repository.associations import ScenarioLiabilityRepo
from app.repository.entities import LiabilityRepo
from .mixin import BaseAssociationService


class ScenarioLiabilityService(BaseAssociationService):
    @classmethod
    def create_scenario_liability(cls, account_id: str, payload: dict) -> dict:
        """Create a new scenario liability assoc with validated owner."""

        scenario_id, liability_id = payload["scenario_id"], payload["liability_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_liability_ownership(account_id=account_id, liability_id=liability_id)

        # Create assoc based on payload
        assoc_domain = ScenarioLiabilityDomain(**payload)
        assoc = ScenarioLiabilityRepo.create(assoc_domain)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc)

    @classmethod
    def get_scenario_liability_by_id(cls, account_id: str, payload: dict) -> dict:
        """Get the scenario liability assoc by id with validated owner."""

        scenario_id, liability_id = payload["scenario_id"], payload["liability_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_liability_ownership(account_id=account_id, liability_id=liability_id)

        # Get assoc by id
        assoc_from_repo = ScenarioLiabilityRepo.get_by_id(
            scenario_id=scenario_id, liability_id=liability_id
        )

        if not assoc_from_repo:
            raise ValueError(
                f"Scenario Liability Association with scenario ID {scenario_id} and liability ID {liability_id} not found"
            )

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc_from_repo)

    @classmethod
    def get_scenario_liabilities(cls, account_id: str, payload: dict) -> list[dict]:
        """Get all scenario liability assoc with validated owner."""

        scenario_id = payload["scenario_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)

        # Generate the list of dict based on the assocs got from the repo
        return [
            cls._create_response(assoc=assoc)
            for assoc in ScenarioLiabilityRepo.get_list(scenario_id=scenario_id)
        ]

    @classmethod
    def update_scenario_liability(cls, account_id: str, payload: dict) -> dict:
        """Update the scenario liability assoc with validated owner."""

        # Get the Scenario Liability Association
        assoc = cls.get_scenario_liability_by_id(
            account_id=account_id, payload=payload
        )["association"]

        # Update the Scenario Liability Association based on given payload
        for field in payload.keys():
            setattr(assoc, field, payload[field])

        # Set the change by repo
        updated_assoc = ScenarioLiabilityRepo.save(assoc)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=updated_assoc)

    @classmethod
    def delete_scenario_liability_by_id(cls, account_id: str, payload: dict) -> str:
        """Delete the scenario liability assoc by ID with validated owner."""
        # Get the Scenario Liability Association
        # Raises if not found or unauthorized
        cls.get_scenario_liability_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Get the scenario and liability ID
        scenario_id, liability_id = payload["scenario_id"], payload["liability_id"]

        # Delete the assoc
        ScenarioLiabilityRepo.delete_by_id(
            scenario_id=scenario_id, liability_id=liability_id
        )

        return f"Scenario Liability with scenario ID {scenario_id} and liability ID {liability_id} deleted successfully"

    @staticmethod
    def _create_response(assoc: ScenarioLiabilityDomain) -> dict:
        return {
            "association": assoc,
            "liability": LiabilityRepo.get_by_id(liability_id=assoc.liability_id),
        }

    @staticmethod
    def _check_liability_ownership(account_id: str, liability_id: str) -> str:
        if not isinstance(liability_id, str):
            raise TypeError(
                f"Liability ID should be type str, not type {type(liability_id).__name__}"
            )

        liability_from_repo = LiabilityRepo.get_by_id(liability_id=liability_id)

        if not liability_from_repo:
            raise ValueError(f"Liability with ID {liability_id} not found")

        if liability_from_repo.owner.id != account_id:
            raise PermissionError(f"Account {account_id} does not own this liability")

        return "This account owned this liability"
