from app.domain.entities import ChildSavingPlanDomain
from app.infrastructure.models import ChildSavingPlan  # , Child, ChildSavingAmountEntry
from app import db
import sqlalchemy as sa
from .base import EntityRepo


class ChildSavingPlanRepo(EntityRepo):
    @staticmethod
    def create(child_saving_plan: ChildSavingPlanDomain) -> ChildSavingPlanDomain:
        """Given a DomainObject, store it in the database and return the stored object."""
        # Instance with required attr
        child_saving_plan_model = ChildSavingPlan(
            name=child_saving_plan.name,
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            setattr(
                child_saving_plan_model, attr, getattr(child_saving_plan, attr, None)
            )

        # Create the child saving amount entries
        saved_child_saving_amount_entries = []
        for entry in child_saving_plan.child_saving_amount_entries:
            pass
            # Save entry to the database
            # saved_child_saving_amount_entries.append(saved_entry)

        # # Get the child saving amount entries orm from database by child_saving_plan ID
        # child_saving_amount_entries = db.session.scalars(
        #     sa.select(ChildSavingAmountEntry).where(ChildSavingAmountEntry.child_saving_plan_id == child_saving_plan.id)
        # ).all()

        child_saving_plan_model.child_saving_amount_entries = (
            saved_child_saving_amount_entries
        )

        # Save the ChildSavingPlan model to the database
        db.session.add(child_saving_plan_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ChildSavingPlanRepo._map_to_domain(child_saving_plan_model)

    @staticmethod
    def save(child_saving_plan: ChildSavingPlanDomain) -> ChildSavingPlanDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get child_saving_plan_model from database
        child_saving_plan_model = db.session.scalar(
            sa.select(ChildSavingPlan).where(ChildSavingPlan.id == child_saving_plan.id)
        )
        if not child_saving_plan_model:
            raise ValueError("ChildSavingPlan not found")

        # Update ChildSavingPlan Model
        child_saving_plan_model.name = child_saving_plan.name
        child_saving_plan_model.child_saving_amount_entries = (
            child_saving_plan.child_saving_amount_entries
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            origin_attr = getattr(child_saving_plan_model, attr)
            setattr(
                child_saving_plan_model,
                attr,
                getattr(child_saving_plan, attr, origin_attr),
            )

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ChildSavingPlanRepo._map_to_domain(child_saving_plan_model)

    @staticmethod
    def get_by_id(child_saving_plan_id: int) -> ChildSavingPlanDomain | None:
        """Retrieve an child_saving_plan by ID and return as DomainObject."""
        # Get child_saving_plan_model from database
        child_saving_plan_model = db.session.scalar(
            sa.select(ChildSavingPlan).where(ChildSavingPlan.id == child_saving_plan_id)
        )
        if not child_saving_plan_model:
            return None

        # Return the domain object with attributes populated from the database
        return ChildSavingPlanRepo._map_to_domain(child_saving_plan_model)

    @staticmethod
    def get_list(account_id: str) -> list[ChildSavingPlanDomain]:
        """Retrieve all child_saving_plan_saving_plans of the account and return as a list of DomainObjects."""
        child_saving_plan_model_list = db.session.scalars(
            sa.select(ChildSavingPlan).where(ChildSavingPlan.parent_id == account_id)
        ).all()
        return [
            ChildSavingPlanRepo._map_to_domain(
                child_saving_plan, child_saving_plan.parent.id
            )
            for child_saving_plan in child_saving_plan_model_list
        ]

    @staticmethod
    def delete_by_id(child_saving_plan_id: int) -> None:
        """Given an child_saving_plan ID, remove it from the database."""
        # Get child_saving_plan_model from database
        child_saving_plan_model = db.session.scalar(
            sa.select(ChildSavingPlan).where(ChildSavingPlan.id == child_saving_plan_id)
        )
        if child_saving_plan_model:
            db.session.delete(child_saving_plan_model)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(
        child_saving_plan_model: ChildSavingPlan, parent_id: str
    ) -> ChildSavingPlanDomain:
        """Helper method to map the ChildSavingPlan model to a Domain Object."""
        # Get child_saving_amount_entries from database
        child_saving_amount_entries_from_db = []
        return ChildSavingPlanDomain(
            id=child_saving_plan_model.id,
            name=child_saving_plan_model.name,
            created_at=child_saving_plan_model.created_at,
            updated_at=child_saving_plan_model.updated_at,
            description=child_saving_plan_model.description,
            child_saving_amount_entries=child_saving_amount_entries_from_db,
        )

    @staticmethod
    def _create_child_saving_amount_entry(
        child_saving_amount_entry: ChildSavingPlanDomain,
    ) -> ChildSavingPlanDomain:
        pass

    @staticmethod
    def _update_child_saving_amount_entry(
        child_saving_amount_entry: ChildSavingPlanDomain,
    ) -> ChildSavingPlanDomain:
        pass

    @staticmethod
    def _get_child_saving_amount_entry_by_id(id: str) -> ChildSavingPlanDomain:
        pass

    @staticmethod
    def _get_child_saving_amount_entries(id: str) -> ChildSavingPlanDomain:
        pass

    @staticmethod
    def _update_child_saving_amount_entry(
        child_saving_amount_entry: ChildSavingPlanDomain,
    ) -> ChildSavingPlanDomain:
        pass
