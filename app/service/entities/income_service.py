from app.domain.entities import IncomeDomain
from app.repository.entities import IncomeRepo
from .mixin import OwnerRequiredServiceMixin


class IncomeService(OwnerRequiredServiceMixin):
    _required_fields = {
        "name",
        "amount",
        "max_yearly_growth_rate",
        "min_yearly_growth_rate",
        "start_age",
    }
    _all_fields = _required_fields | {
        "description",
        "end_age",
    }

    @staticmethod
    def create_income(account_id: str, payload: dict) -> IncomeDomain:
        """Create a new income with validated owner."""

        owner_id = payload["owner_id"]

        # Check if account_id matches the owner_id
        if owner_id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authorized to create income under the given owner"
            )

        # Validate required fields
        missing_fields = IncomeService._required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Get owner
        owner = IncomeService._get_owner(owner_id)

        # Filter payload to only include allowed fields
        income_payload = {
            field: payload[field]
            for field in IncomeService._all_fields
            if field in payload
        }
        income_payload["owner"] = owner

        # Create the income
        income = IncomeDomain(**income_payload)
        return IncomeRepo.create(income)

    @classmethod
    def get_income_by_id(cls, account_id: str, payload: dict) -> IncomeDomain:
        """Retrieve a specific income by ID."""
        income_id = payload.get("id")
        if not income_id:
            raise ValueError("Income ID is required")
        income_from_repo = IncomeRepo.get_by_id(income_id)

        if not income_from_repo:
            raise ValueError(f"Income with ID {income_id} not found")

        # Check if the account owns the income
        cls._check_ownership_by_id(
            account_id=account_id, owner_id=income_from_repo.owner.id
        )

        return income_from_repo

    @staticmethod
    def get_incomes(account_id: str) -> list[IncomeDomain]:
        """Retrieve all incomes for a given account."""
        return IncomeRepo.get_list(account_id)

    @staticmethod
    def update_income(account_id: str, payload: dict) -> IncomeDomain:
        """Update an income by ID if it exists."""
        income_from_repo = IncomeService.get_income_by_id(account_id, payload)

        for field in IncomeService._all_fields:
            if field in payload:
                setattr(income_from_repo, field, payload[field])

        return IncomeRepo.save(income_from_repo)

    @staticmethod
    def delete_income_by_id(account_id: str, payload: dict) -> str:
        """Delete an income by ID if it exists."""
        income = IncomeService.get_income_by_id(
            account_id, payload
        )  # Raises if not found or unauthorized
        IncomeRepo.delete_by_id(income.id)
        return f"Income {income.id} deleted successfully"
