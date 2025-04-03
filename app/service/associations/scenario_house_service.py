from app.domain.associations import ScenarioHouseDomain
from app.repository.associations import ScenarioHouseRepo
from app.repository.entities import HouseRepo
from .mixin import BaseAssociationService


class ScenarioHouseService(BaseAssociationService):
    @classmethod
    def create_scenario_house(cls, account_id: str, payload: dict) -> dict:
        """Create a new scenario house assoc with validated owner."""

        scenario_id, house_id = payload["scenario_id"], payload["house_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_house_ownership(account_id=account_id, house_id=house_id)

        # Create assoc based on payload
        assoc_domain = ScenarioHouseDomain(**payload)
        assoc = ScenarioHouseRepo.create(assoc_domain)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc)

    @classmethod
    def get_scenario_house_by_id(cls, account_id: str, payload: dict) -> dict:
        """Get the scenario house assoc by id with validated owner."""

        scenario_id, house_id = payload["scenario_id"], payload["house_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_house_ownership(account_id=account_id, house_id=house_id)

        # Get assoc by id
        assoc_from_repo = ScenarioHouseRepo.get_by_id(
            scenario_id=scenario_id, house_id=house_id
        )

        if not assoc_from_repo:
            raise ValueError(
                f"Scenario House Association with scenario ID {scenario_id} and house ID {house_id} not found"
            )

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc_from_repo)

    @classmethod
    def get_scenario_houses(cls, account_id: str, payload: dict) -> list[dict]:
        """Get all scenario house assoc with validated owner."""

        scenario_id = payload["scenario_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)

        # Generate the list of dict based on the assocs got from the repo
        return [
            cls._create_response(assoc=assoc)
            for assoc in ScenarioHouseRepo.get_list(scenario_id=scenario_id)
        ]

    @classmethod
    def update_scenario_house(cls, account_id: str, payload: dict) -> dict:
        """Update the scenario house assoc with validated owner."""

        # Get the Scenario House Association
        assoc = cls.get_scenario_house_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Update the Scenario House Association based on given payload
        for field in payload.keys():
            setattr(assoc, field, payload[field])

        # Set the change by repo
        updated_assoc = ScenarioHouseRepo.save(assoc)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=updated_assoc)

    @classmethod
    def delete_scenario_house_by_id(cls, account_id: str, payload: dict) -> str:
        """Delete the scenario house assoc by ID with validated owner."""
        # Get the Scenario House Association
        # Raises if not found or unauthorized
        cls.get_scenario_house_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Get the scenario and house ID
        scenario_id, house_id = payload["scenario_id"], payload["house_id"]

        # Delete the assoc
        ScenarioHouseRepo.delete_by_id(scenario_id=scenario_id, house_id=house_id)

        return f"Scenario House with scenario ID {scenario_id} and house ID {house_id} deleted successfully"

    @staticmethod
    def _create_response(assoc: ScenarioHouseDomain) -> dict:
        return {
            "association": assoc,
            "house": HouseRepo.get_by_id(house_id=assoc.house_id),
        }

    @staticmethod
    def _check_house_ownership(account_id: str, house_id: str) -> str:
        if not isinstance(house_id, str):
            raise TypeError(
                f"House ID should be type str, not type {type(house_id).__name__}"
            )

        house_from_repo = HouseRepo.get_by_id(house_id=house_id)

        if not house_from_repo:
            raise ValueError(f"House with ID {house_id} not found")

        if house_from_repo.owner.id != account_id:
            raise PermissionError(f"Account {account_id} does not own this house")

        return "This account owned this house"
