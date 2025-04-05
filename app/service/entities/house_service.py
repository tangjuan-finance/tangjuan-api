from app.domain.entities import HouseDomain
from app.repository.entities import HouseRepo
from .mixin import OwnerRequiredServiceMixin


class HouseService(OwnerRequiredServiceMixin):
    _required_fields = {
        "name",
        "amount",
        "down_payment",
        "interest_rate",
        "loan_term",
        "purchase_age",
    }
    _all_fields = _required_fields | {
        "description",
        "sale_age",
    }

    @staticmethod
    def create_house(account_id: str, payload: dict) -> HouseDomain:
        """Create a new house with validated owner."""

        owner_id = payload["owner_id"]

        # Check if account_id matches the owner_id
        if owner_id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authorized to create house under the given owner"
            )

        # Validate required fields
        missing_fields = HouseService._required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Get owner
        owner = HouseService._get_owner(owner_id)

        # Filter payload to only include allowed fields
        house_payload = {
            field: payload[field]
            for field in HouseService._all_fields
            if field in payload
        }
        house_payload["owner"] = owner

        # Create the house
        house = HouseDomain(**house_payload)
        return HouseRepo.create(house)

    @classmethod
    def get_house_by_id(cls, account_id: str, payload: dict) -> HouseDomain:
        """Retrieve a specific house by ID."""
        house_id = payload.get("id")
        if not house_id:
            raise ValueError("House ID is required")
        house_from_repo = HouseRepo.get_by_id(house_id)

        if not house_from_repo:
            raise ValueError(f"House with ID {house_id} not found")

        # Check if the account owns the house
        cls._check_ownership_by_id(
            account_id=account_id, owner_id=house_from_repo.owner.id
        )

        return house_from_repo

    @staticmethod
    def get_houses(account_id: str) -> list[HouseDomain]:
        """Retrieve all houses for a given account."""
        return HouseRepo.get_list(account_id)

    @staticmethod
    def update_house(account_id: str, payload: dict) -> HouseDomain:
        """Update an house by ID if it exists."""
        house_from_repo = HouseService.get_house_by_id(account_id, payload)

        for field in HouseService._all_fields:
            if field in payload:
                setattr(house_from_repo, field, payload[field])

        return HouseRepo.save(house_from_repo)

    @staticmethod
    def delete_house_by_id(account_id: str, payload: dict) -> str:
        """Delete an house by ID if it exists."""
        house = HouseService.get_house_by_id(
            account_id, payload
        )  # Raises if not found or unauthorized
        HouseRepo.delete_by_id(house.id)
        return f"House {house.id} deleted successfully"
