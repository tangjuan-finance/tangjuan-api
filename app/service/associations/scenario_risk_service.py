from app.domain.associations import ScenarioRiskDomain
from app.repository.associations import ScenarioRiskRepo
from app.repository.entities import RiskRepo
from .base import BaseAssociationService


class ScenarioRiskService(BaseAssociationService):
    @classmethod
    def create_scenario_risk(cls, account_id: str, payload: dict) -> dict:
        """Create a new scenario risk assoc with validated owner."""

        scenario_id, risk_id = payload["scenario_id"], payload["risk_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_risk_ownership(account_id=account_id, risk_id=risk_id)

        # Create assoc based on payload
        assoc_domain = ScenarioRiskDomain(**payload)
        assoc = ScenarioRiskRepo.create(assoc_domain)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc)

    @classmethod
    def get_scenario_risk_by_id(cls, account_id: str, payload: dict) -> dict:
        """Get the scenario risk assoc by id with validated owner."""

        scenario_id, risk_id = payload["scenario_id"], payload["risk_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_risk_ownership(account_id=account_id, risk_id=risk_id)

        # Get assoc by id
        assoc_from_repo = ScenarioRiskRepo.get_by_id(
            scenario_id=scenario_id, risk_id=risk_id
        )

        if not assoc_from_repo:
            raise ValueError(
                f"Scenario Risk Association with scenario ID {scenario_id} and risk ID {risk_id} not found"
            )

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc_from_repo)

    @classmethod
    def get_scenario_risks(cls, account_id: str, payload: dict) -> list[dict]:
        """Get all scenario risk assoc with validated owner."""

        scenario_id = payload["scenario_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)

        # Generate the list of dict based on the assocs got from the repo
        return [
            cls._create_response(assoc=assoc)
            for assoc in ScenarioRiskRepo.get_list(scenario_id=scenario_id)
        ]

    @classmethod
    def update_scenario_risk(cls, account_id: str, payload: dict) -> dict:
        """Update the scenario risk assoc with validated owner."""

        # Get the Scenario Risk Association
        assoc = cls.get_scenario_risk_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Update the Scenario Risk Association based on given payload
        for field in payload.keys():
            setattr(assoc, field, payload[field])

        # Set the change by repo
        updated_assoc = ScenarioRiskRepo.save(assoc)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=updated_assoc)

    @classmethod
    def delete_scenario_risk_by_id(cls, account_id: str, payload: dict) -> str:
        """Delete the scenario risk assoc by ID with validated owner."""
        # Get the Scenario Risk Association
        # Raises if not found or unauthorized
        cls.get_scenario_risk_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Get the scenario and risk ID
        scenario_id, risk_id = payload["scenario_id"], payload["risk_id"]

        # Delete the assoc
        ScenarioRiskRepo.delete_by_id(scenario_id=scenario_id, risk_id=risk_id)

        return f"Scenario Risk with scenario ID {scenario_id} and risk ID {risk_id} deleted successfully"

    @staticmethod
    def _create_response(assoc: ScenarioRiskDomain) -> dict:
        return {
            "association": assoc,
            "risk": RiskRepo.get_by_id(risk_id=assoc.risk_id),
        }

    @classmethod
    def _check_risk_ownership(cls, account_id: str, risk_id: str) -> str:
        if not isinstance(risk_id, str):
            raise TypeError(
                f"Risk ID should be type str, not type {type(risk_id).__name__}"
            )

        risk_from_repo = RiskRepo.get_by_id(risk_id=risk_id)

        if not risk_from_repo:
            raise ValueError(f"Risk with ID {risk_id} not found")

        cls._check_ownership_by_id(
            account_id=account_id, owner_id=risk_from_repo.owner.id
        )

        return "This account owned this risk"
