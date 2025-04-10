from app.domain.associations import ScenarioChildDomain
from app.repository.associations import ScenarioChildRepo
from app.repository.entities import ChildRepo
from .base import BaseAssociationService


class ScenarioChildService(BaseAssociationService):
    @classmethod
    def create_scenario_child(cls, account_id: str, payload: dict) -> dict:
        """Create a new scenario child assoc with validated parent."""

        scenario_id, child_id = payload["scenario_id"], payload["child_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_child_parentship(account_id=account_id, child_id=child_id)

        # Create assoc based on payload
        assoc_domain = ScenarioChildDomain(**payload)
        assoc = ScenarioChildRepo.create(assoc_domain)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc)

    @classmethod
    def get_scenario_child_by_id(cls, account_id: str, payload: dict) -> dict:
        """Get the scenario child assoc by id with validated parent."""

        scenario_id, child_id = payload["scenario_id"], payload["child_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_child_parentship(account_id=account_id, child_id=child_id)

        # Get assoc by id
        assoc_from_repo = ScenarioChildRepo.get_by_id(
            scenario_id=scenario_id, child_id=child_id
        )

        if not assoc_from_repo:
            raise ValueError(
                f"Scenario Child Association with scenario ID {scenario_id} and child ID {child_id} not found"
            )

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc_from_repo)

    @classmethod
    def get_scenario_children(cls, account_id: str, payload: dict) -> list[dict]:
        """Get all scenario child assoc with validated parent."""

        scenario_id = payload["scenario_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)

        # Generate the list of dict based on the assocs got from the repo
        return [
            cls._create_response(assoc=assoc)
            for assoc in ScenarioChildRepo.get_list(scenario_id=scenario_id)
        ]

    @classmethod
    def update_scenario_child(cls, account_id: str, payload: dict) -> dict:
        """Update the scenario child assoc with validated parent."""

        # Get the Scenario Child Association
        assoc = cls.get_scenario_child_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Update the Scenario Child Association based on given payload
        for field in payload.keys():
            setattr(assoc, field, payload[field])

        # Set the change by repo
        updated_assoc = ScenarioChildRepo.save(assoc)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=updated_assoc)

    @classmethod
    def delete_scenario_child_by_id(cls, account_id: str, payload: dict) -> str:
        """Delete the scenario child assoc by ID with validated parent."""
        # Get the Scenario Child Association
        # Raises if not found or unauthorized
        cls.get_scenario_child_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Get the scenario and child ID
        scenario_id, child_id = payload["scenario_id"], payload["child_id"]

        # Delete the assoc
        ScenarioChildRepo.delete_by_id(scenario_id=scenario_id, child_id=child_id)

        return f"Scenario Child with scenario ID {scenario_id} and child ID {child_id} deleted successfully"

    @staticmethod
    def _create_response(assoc: ScenarioChildDomain) -> dict:
        return {
            "association": assoc,
            "child": ChildRepo.get_by_id(child_id=assoc.child_id),
        }

    @classmethod
    def _check_child_parentship(cls, account_id: str, child_id: str) -> str:
        if not isinstance(child_id, str):
            raise TypeError(
                f"Child ID should be type str, not type {type(child_id).__name__}"
            )

        child_from_repo = ChildRepo.get_by_id(child_id=child_id)

        if not child_from_repo:
            raise ValueError(f"Child with ID {child_id} not found")

        cls._check_entity_ownership_by_id(
            account_id=account_id, owner_id=child_from_repo.parent.id
        )

        return "This account owned this child"
