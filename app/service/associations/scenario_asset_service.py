from app.domain.associations import ScenarioAssetDomain
from app.repository.associations import ScenarioAssetRepo
from app.repository.entities import AssetRepo
from .base import BaseAssociationService


class ScenarioAssetService(BaseAssociationService):
    @classmethod
    def create_scenario_asset(cls, account_id: str, payload: dict) -> dict:
        """Create a new scenario asset assoc with validated owner."""

        scenario_id, asset_id = payload["scenario_id"], payload["asset_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_asset_ownership(account_id=account_id, asset_id=asset_id)

        # Create assoc based on payload
        assoc_domain = ScenarioAssetDomain(**payload)
        assoc = ScenarioAssetRepo.create(assoc_domain)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc)

    @classmethod
    def get_scenario_asset_by_id(cls, account_id: str, payload: dict) -> dict:
        """Get the scenario asset assoc by id with validated owner."""

        scenario_id, asset_id = payload["scenario_id"], payload["asset_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_asset_ownership(account_id=account_id, asset_id=asset_id)

        # Get assoc by id
        assoc_from_repo = ScenarioAssetRepo.get_by_id(
            scenario_id=scenario_id, asset_id=asset_id
        )

        if not assoc_from_repo:
            raise ValueError(
                f"Scenario Asset Association with scenario ID {scenario_id} and asset ID {asset_id} not found"
            )

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc_from_repo)

    @classmethod
    def get_scenario_assets(cls, account_id: str, payload: dict) -> list[dict]:
        """Get all scenario asset assoc with validated owner."""

        scenario_id = payload["scenario_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)

        # Generate the list of dict based on the assocs got from the repo
        return [
            cls._create_response(assoc=assoc)
            for assoc in ScenarioAssetRepo.get_list(scenario_id=scenario_id)
        ]

    @classmethod
    def update_scenario_asset(cls, account_id: str, payload: dict) -> dict:
        """Update the scenario asset assoc with validated owner."""

        # Get the Scenario Asset Association
        assoc = cls.get_scenario_asset_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Update the Scenario Asset Association based on given payload
        for field in payload.keys():
            setattr(assoc, field, payload[field])

        # Set the change by repo
        updated_assoc = ScenarioAssetRepo.save(assoc)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=updated_assoc)

    @classmethod
    def delete_scenario_asset_by_id(cls, account_id: str, payload: dict) -> str:
        """Delete the scenario asset assoc by ID with validated owner."""
        # Get the Scenario Asset Association
        # Raises if not found or unauthorized
        cls.get_scenario_asset_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Get the scenario and asset ID
        scenario_id, asset_id = payload["scenario_id"], payload["asset_id"]

        # Delete the assoc
        ScenarioAssetRepo.delete_by_id(scenario_id=scenario_id, asset_id=asset_id)

        return f"Scenario Asset with scenario ID {scenario_id} and asset ID {asset_id} deleted successfully"

    @staticmethod
    def _create_response(assoc: ScenarioAssetDomain) -> dict:
        return {
            "association": assoc,
            "asset": AssetRepo.get_by_id(asset_id=assoc.asset_id),
        }

    @staticmethod
    def _check_asset_ownership(account_id: str, asset_id: str) -> str:
        if not isinstance(asset_id, str):
            raise TypeError(
                f"Asset ID should be type str, not type {type(asset_id).__name__}"
            )

        asset_from_repo = AssetRepo.get_by_id(asset_id=asset_id)

        if not asset_from_repo:
            raise ValueError(f"Asset with ID {asset_id} not found")

        if asset_from_repo.owner.id != account_id:
            raise PermissionError(f"Account {account_id} does not own this asset")

        return "This account owned this asset"
