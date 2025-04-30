from app.domain.entities import ChildSavingPlanDomain, ChildSavingAmountEntryDomain
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

    _entry_required_fields = {
        "name",
        "start_age",
        "end_age",
        "amount",
    }
    _entry_all_fields = _entry_required_fields | {
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

    # === The following is for the amount entry

    @staticmethod
    def _get_plan_by_id(account_id: str, plan_id: str) -> ChildSavingPlanDomain:
        return ChildSavingPlanService.get_child_saving_plan_by_id(
            account_id,
            {
                "id": plan_id,
            },
        )

    @staticmethod
    def add_amount_entry(
        account_id: str, plan_id: str, payload: dict
    ) -> ChildSavingAmountEntryDomain:
        """Create a new entry with validated owner and plan"""

        # Get plan by service to ensure validation
        plan = ChildSavingPlanService._get_plan_by_id(account_id, plan_id)

        # Validate required fields
        missing_fields = ChildSavingPlanService._entry_required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Filter payload to only include allowed fields
        entry_payload = {
            field: payload[field]
            for field in ChildSavingPlanService._entry_all_fields
            if field in payload
        }

        entry = plan.add_entry(**entry_payload)

        # Save the entry to the db
        updated_plan = ChildSavingPlanRepo.save(plan)

        # Return the saved entry
        return updated_plan.get_entry_by_id(entry.id)

    @staticmethod
    def get_amount_entry_by_id(
        account_id: str, plan_id: str, entry_id: str
    ) -> ChildSavingAmountEntryDomain:
        """Get an entry by id"""

        # Get plan by service to ensure validation
        plan = ChildSavingPlanService._get_plan_by_id(account_id, plan_id)
        entry = plan.get_entry_by_id(entry_id)

        # Raise Value Error of entry not existed
        if not entry:
            raise ValueError(f"Entry with ID {entry_id} not existed")

        return entry

    @staticmethod
    def list_amount_entries(
        account_id: str, plan_id: str
    ) -> list[ChildSavingAmountEntryDomain]:
        """Get entries belongs to given plan"""

        # Get plan by service to ensure validation
        plan = ChildSavingPlanService._get_plan_by_id(account_id, plan_id)

        return plan.list_entries()

    @staticmethod
    def update_amount_entry_by_id(
        account_id: str, plan_id: str, entry_id: str, payload: dict
    ) -> ChildSavingAmountEntryDomain:
        """Update an entry by id"""
        # Get plan by service to ensure validation
        plan = ChildSavingPlanService._get_plan_by_id(account_id, plan_id)
        entry = plan.get_entry_by_id(entry_id)

        # Raise Value Error of entry not existed
        if not entry:
            raise ValueError(f"Entry with ID {entry_id} not existed")

        valid_payload = {
            field: payload[field]
            for field in ChildSavingPlanService._entry_all_fields
            if field in payload
        }

        plan.update_entry_by_id(entry.id, **valid_payload)

        # Save the updated plan to the db
        updated_plan = ChildSavingPlanRepo.save(plan)

        # Return the saved entry
        return updated_plan.get_entry_by_id(entry.id)

    @staticmethod
    def remove_amount_entry_by_id(account_id: str, plan_id: str, entry_id: str) -> None:
        """Remove an entry by id"""
        # Get plan by service to ensure validation
        plan = ChildSavingPlanService._get_plan_by_id(account_id, plan_id)
        entry = plan.get_entry_by_id(entry_id)

        # Raise Value Error of entry not existed
        if not entry:
            raise ValueError(f"Entry with ID {entry_id} not existed")

        plan.remove_entry_by_id(entry.id)

        # Save the updated plan to the db
        updated_plan = ChildSavingPlanRepo.save(plan)

        # Return the saved entry
        return updated_plan.get_entry_by_id(entry.id)
