from app.domain.entities import ChildSavingPlanDomain
from app.repository.entities import ChildSavingPlanRepo
from .mixin import OwnerRequiredServiceMixin


class ChildSavingPlanService(OwnerRequiredServiceMixin):
    _required_fields = {
        "name",
        "independent_age",
    }
    _all_fields = _required_fields | {
        "description",
    }

    @staticmethod
    def create_child_saving_plan(
        account_id: str, payload: dict
    ) -> ChildSavingPlanDomain:
        """Create a new child_saving_plan with validated owner."""

        owner_id = payload["owner_id"]

        # Check if account_id matches the owner_id
        if owner_id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authorized to create child_saving_plan under the given owner"
            )

        # Validate required fields
        missing_fields = ChildSavingPlanService._required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Filter payload to only include allowed fields
        child_saving_plan_payload = {
            field: payload[field]
            for field in ChildSavingPlanService._all_fields
            if field in payload
        }
        child_saving_plan_payload["owner_id"] = owner_id

        # Create the child_saving_plan
        child_saving_plan = ChildSavingPlanDomain(**child_saving_plan_payload)
        return ChildSavingPlanRepo.create(child_saving_plan)

    @classmethod
    def get_child_saving_plan_by_id(
        cls, account_id: str, payload: dict
    ) -> ChildSavingPlanDomain:
        """Retrieve a specific child_saving_plan by ID."""
        child_saving_plan_id = payload.get("id")
        if not child_saving_plan_id:
            raise ValueError("ChildSavingPlan ID is required")
        child_saving_plan_from_repo = ChildSavingPlanRepo.get_by_id(
            child_saving_plan_id
        )

        if not child_saving_plan_from_repo:
            raise ValueError(
                f"ChildSavingPlan with ID {child_saving_plan_id} not found"
            )

        # Check if the account owns the child_saving_plan
        cls._check_entity_ownership_by_id(
            account_id=account_id, owner_id=child_saving_plan_from_repo.owner_id
        )

        return child_saving_plan_from_repo

    @staticmethod
    def get_child_saving_plans(account_id: str) -> list[ChildSavingPlanDomain]:
        """Retrieve all child_saving_plans for a given account."""
        return ChildSavingPlanRepo.get_list(account_id)

    @staticmethod
    def update_child_saving_plan(
        account_id: str, payload: dict
    ) -> ChildSavingPlanDomain:
        """Update an child_saving_plan by ID if it exists."""
        child_saving_plan_from_repo = (
            ChildSavingPlanService.get_child_saving_plan_by_id(account_id, payload)
        )

        for field in ChildSavingPlanService._all_fields:
            if field in payload:
                setattr(child_saving_plan_from_repo, field, payload[field])

        return ChildSavingPlanRepo.save(child_saving_plan_from_repo)

    @staticmethod
    def delete_child_saving_plan_by_id(account_id: str, payload: dict) -> str:
        """Delete an child_saving_plan by ID if it exists."""
        child_saving_plan = ChildSavingPlanService.get_child_saving_plan_by_id(
            account_id, payload
        )  # Raises if not found or unauthorized
        ChildSavingPlanRepo.delete_by_id(child_saving_plan.id)
        return f"ChildSavingPlan {child_saving_plan.id} deleted successfully"
