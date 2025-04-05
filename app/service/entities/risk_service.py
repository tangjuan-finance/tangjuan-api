from app.domain.entities import RiskDomain
from app.repository.entities import RiskRepo
from .mixin import OwnerRequiredServiceMixin


class RiskService(OwnerRequiredServiceMixin):
    _required_fields = {
        "name",
        "max_loss",
        "min_loss",
        "start_age",
    }
    _all_fields = _required_fields | {
        "description",
        "end_age",
    }

    @staticmethod
    def create_risk(account_id: str, payload: dict) -> RiskDomain:
        """Create a new risk with validated owner."""

        owner_id = payload["owner_id"]

        # Check if account_id matches the owner_id
        if owner_id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authorized to create risk under the given owner"
            )

        # Validate required fields
        missing_fields = RiskService._required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Get owner
        owner = RiskService._get_owner(owner_id)

        # Filter payload to only include allowed fields
        risk_payload = {
            field: payload[field]
            for field in RiskService._all_fields
            if field in payload
        }
        risk_payload["owner"] = owner

        # Create the risk
        risk = RiskDomain(**risk_payload)
        return RiskRepo.create(risk)

    @classmethod
    def get_risk_by_id(cls, account_id: str, payload: dict) -> RiskDomain:
        """Retrieve a specific risk by ID."""
        risk_id = payload.get("id")
        if not risk_id:
            raise ValueError("Risk ID is required")
        risk_from_repo = RiskRepo.get_by_id(risk_id)

        if not risk_from_repo:
            raise ValueError(f"Risk with ID {risk_id} not found")

        # Check if the account owns the risk
        cls._check_ownership_by_id(
            account_id=account_id, owner_id=risk_from_repo.owner.id
        )

        return risk_from_repo

    @staticmethod
    def get_risks(account_id: str) -> list[RiskDomain]:
        """Retrieve all risks for a given account."""
        return RiskRepo.get_list(account_id)

    @staticmethod
    def update_risk(account_id: str, payload: dict) -> RiskDomain:
        """Update an risk by ID if it exists."""
        risk_from_repo = RiskService.get_risk_by_id(account_id, payload)

        for field in RiskService._all_fields:
            if field in payload:
                setattr(risk_from_repo, field, payload[field])

        return RiskRepo.save(risk_from_repo)

    @staticmethod
    def delete_risk_by_id(account_id: str, payload: dict) -> str:
        """Delete an risk by ID if it exists."""
        risk = RiskService.get_risk_by_id(
            account_id, payload
        )  # Raises if not found or unauthorized
        RiskRepo.delete_by_id(risk.id)
        return f"Risk {risk.id} deleted successfully"
