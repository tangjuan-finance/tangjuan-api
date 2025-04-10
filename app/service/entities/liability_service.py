from app.domain.entities import LiabilityDomain
from app.repository.entities import LiabilityRepo
from .mixin import OwnerRequiredServiceMixin


class LiabilityService(OwnerRequiredServiceMixin):
    _required_fields = {
        "name",
        "principal_amount",
        "interest_rate",
        "start_age",
        "end_age",
    }
    _all_fields = _required_fields | {
        "description",
    }

    @staticmethod
    def create_liability(account_id: str, payload: dict) -> LiabilityDomain:
        """Create a new liability with validated owner."""

        owner_id = payload["owner_id"]

        # Check if account_id matches the owner_id
        if owner_id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authorized to create liability under the given owner"
            )

        # Validate required fields
        missing_fields = LiabilityService._required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Get owner
        owner = LiabilityService._get_owner(owner_id)

        # Filter payload to only include allowed fields
        liability_payload = {
            field: payload[field]
            for field in LiabilityService._all_fields
            if field in payload
        }
        liability_payload["owner"] = owner

        # Create the liability
        liability = LiabilityDomain(**liability_payload)
        return LiabilityRepo.create(liability)

    @classmethod
    def get_liability_by_id(cls, account_id: str, payload: dict) -> LiabilityDomain:
        """Retrieve a specific liability by ID."""
        liability_id = payload["id"]
        liability_from_repo = LiabilityRepo.get_by_id(liability_id)

        if not liability_from_repo:
            raise ValueError(f"Liability with ID {liability_id} not found")

        # Check if the account owns the liability
        cls._check_entity_ownership_by_id(
            account_id=account_id, owner_id=liability_from_repo.owner.id
        )

        return liability_from_repo

    @staticmethod
    def get_liabilities(account_id: str) -> list[LiabilityDomain]:
        """Retrieve all liabilities for a given account."""
        return LiabilityRepo.get_list(account_id)

    @staticmethod
    def update_liability(account_id: str, payload: dict) -> LiabilityDomain:
        """Update an liability by ID if it exists."""
        liability_from_repo = LiabilityService.get_liability_by_id(account_id, payload)

        for field in LiabilityService._all_fields:
            if field in payload:
                setattr(liability_from_repo, field, payload[field])

        return LiabilityRepo.save(liability_from_repo)

    @staticmethod
    def delete_liability_by_id(account_id: str, payload: dict) -> str:
        """Delete an liability by ID if it exists."""
        liability = LiabilityService.get_liability_by_id(
            account_id, payload
        )  # Raises if not found or unauthorized
        LiabilityRepo.delete_by_id(liability.id)
        return f"Liability {liability.id} deleted successfully"
