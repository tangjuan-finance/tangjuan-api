from app.domain.entities import AssetDomain
from app.repository.entities import AssetRepo
from .mixin import OwnerRequiredServiceMixin


class AssetService(OwnerRequiredServiceMixin):
    _required_fields = {
        "name",
        "amount",
        "max_yearly_return_rate",
        "min_yearly_return_rate",
        "start_age",
    }
    _all_fields = _required_fields | {
        "description",
        "end_age",
    }

    @staticmethod
    def create_asset(account_id: str, payload: dict) -> AssetDomain:
        """Create a new asset with validated owner."""

        owner_id = payload["owner_id"]

        # Check if account_id matches the owner_id
        if owner_id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authorized to create asset under the given owner"
            )

        # Validate required fields
        missing_fields = AssetService._required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Get owner
        owner = AssetService._get_owner(owner_id)

        # Filter payload to only include allowed fields
        asset_payload = {
            field: payload[field]
            for field in AssetService._all_fields
            if field in payload
        }
        asset_payload["owner"] = owner

        # Create the asset
        asset = AssetDomain(**asset_payload)
        return AssetRepo.create(asset)

    @classmethod
    def get_asset_by_id(cls, account_id: str, payload: dict) -> AssetDomain:
        """Retrieve a specific asset by ID."""
        asset_id = payload.get("id")
        if not asset_id:
            raise ValueError("Asset ID is required")
        asset_from_repo = AssetRepo.get_by_id(asset_id)

        if not asset_from_repo:
            raise ValueError(f"Asset with ID {asset_id} not found")

        # Check if the account owns the asset
        cls._check_entity_ownership_by_id(
            account_id=account_id, owner_id=asset_from_repo.owner.id
        )

        return asset_from_repo

    @staticmethod
    def get_assets(account_id: str) -> list[AssetDomain]:
        """Retrieve all assets for a given account."""
        return AssetRepo.get_list(account_id)

    @staticmethod
    def update_asset(account_id: str, payload: dict) -> AssetDomain:
        """Update an asset by ID if it exists."""
        asset_from_repo = AssetService.get_asset_by_id(account_id, payload)

        for field in AssetService._all_fields:
            if field in payload:
                setattr(asset_from_repo, field, payload[field])

        return AssetRepo.save(asset_from_repo)

    @staticmethod
    def delete_asset_by_id(account_id: str, payload: dict) -> str:
        """Delete an asset by ID if it exists."""
        asset = AssetService.get_asset_by_id(
            account_id, payload
        )  # Raises if not found or unauthorized
        AssetRepo.delete_by_id(asset.id)
        return f"Asset {asset.id} deleted successfully"
