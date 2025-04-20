from app.domain.entities import ChildDomain
from app.repository.entities import ChildRepo
from .mixin import OwnerRequiredServiceMixin


class ChildService(OwnerRequiredServiceMixin):
    _required_fields = {
        "name",
        "birth_age",
        "child_saving_plan_id",
    }
    _all_fields = _required_fields | {
        "description",
    }

    @staticmethod
    def _get_parent(parent_id: str):
        return ChildService._get_owner(parent_id)

    @staticmethod
    def create_child(account_id: str, payload: dict) -> ChildDomain:
        """Create a new child with validated parent."""

        parent_id = payload["parent_id"]

        # Check if account_id matches the parent_id
        if parent_id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authorized to create child under the given parent"
            )

        # Validate required fields
        missing_fields = ChildService._required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Get parent
        parent = ChildService._get_parent(parent_id)

        # Filter payload to only include allowed fields
        child_payload = {
            field: payload[field]
            for field in ChildService._all_fields
            if field in payload
        }
        child_payload["parent"] = parent

        # Create the child
        child = ChildDomain(**child_payload)
        return ChildRepo.create(child)

    @classmethod
    def get_child_by_id(cls, account_id: str, payload: dict) -> ChildDomain:
        """Retrieve a specific child by ID."""
        child_id = payload.get("id")
        if not child_id:
            raise ValueError("Child ID is required")
        child_from_repo = ChildRepo.get_by_id(child_id)

        if not child_from_repo:
            raise ValueError(f"Child with ID {child_id} not found")

        # Check if the account owns the child
        cls._check_entity_ownership_by_id(
            account_id=account_id, owner_id=child_from_repo.parent.id
        )

        return child_from_repo

    @staticmethod
    def get_children(account_id: str) -> list[ChildDomain]:
        """Retrieve all children for a given account."""
        return ChildRepo.get_list(account_id)

    @staticmethod
    def update_child(account_id: str, payload: dict) -> ChildDomain:
        """Update an child by ID if it exists."""
        child_from_repo = ChildService.get_child_by_id(account_id, payload)

        for field in ChildService._all_fields:
            if field in payload:
                setattr(child_from_repo, field, payload[field])

        return ChildRepo.save(child_from_repo)

    @staticmethod
    def delete_child_by_id(account_id: str, payload: dict) -> str:
        """Delete an child by ID if it exists."""
        child = ChildService.get_child_by_id(
            account_id, payload
        )  # Raises if not found or unauthorized
        ChildRepo.delete_by_id(child.id)
        return f"Child {child.id} deleted successfully"
