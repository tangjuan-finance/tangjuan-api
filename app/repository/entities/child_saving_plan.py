from app.domain.entities import ChildSavingPlanDomain, ChildSavingAmountEntryDomain
from app.infrastructure.models import ChildSavingPlan, ChildSavingAmountEntry
from app import db
import sqlalchemy as sa
from .base import EntityRepo


class ChildSavingPlanRepo(EntityRepo):
    @staticmethod
    def create(child_saving_plan: ChildSavingPlanDomain) -> ChildSavingPlanDomain:
        """Given a DomainObject, store it in the database and return the stored object."""
        # Instance with required attr
        child_saving_plan_model = ChildSavingPlan(
            id=child_saving_plan.id,
            name=child_saving_plan.name,
            independent_age=child_saving_plan.independent_age,
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            setattr(
                child_saving_plan_model, attr, getattr(child_saving_plan, attr, None)
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
        child_saving_plan_model.independent_age = child_saving_plan.independent_age
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
            sa.select(ChildSavingPlan).where(ChildSavingPlan.owner_id == account_id)
        ).all()
        return [
            ChildSavingPlanRepo._map_to_domain(child_saving_plan)
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
        child_saving_plan_model: ChildSavingPlan,
    ) -> ChildSavingPlanDomain:
        """Helper method to map the ChildSavingPlan model to a Domain Object."""
        # Get child_saving_amount_entries from database
        child_saving_amount_entries_domain_from_repo = ChildSavingPlanRepo.list_entries(
            child_saving_plan_id=child_saving_plan_model.id
        )
        return ChildSavingPlanDomain(
            _id=child_saving_plan_model.id,
            owner_id=child_saving_plan_model.owner_id,
            name=child_saving_plan_model.name,
            independent_age=child_saving_plan_model.independent_age,
            created_at=child_saving_plan_model.created_at,
            updated_at=child_saving_plan_model.updated_at,
            description=child_saving_plan_model.description,
            child_saving_amount_entries=child_saving_amount_entries_domain_from_repo,
        )

    @staticmethod
    def add_entry(
        entry: ChildSavingAmountEntryDomain,
    ) -> ChildSavingAmountEntryDomain:
        """Given a ChildSavingAmountEntryDomain object, store it in the database and return the stored ChildSavingAmountEntryDomain object."""
        # Instance with required attr
        entry_model = ChildSavingAmountEntry(
            name=entry.name,
            start_age=entry.start_age,
            end_age=entry.end_age,
            amount=entry.amount,
            child_saving_plan_id=entry.child_saving_plan_id,
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            setattr(entry_model, attr, getattr(entry, attr, None))

        # Save the ChildSavingPlan model to the database
        db.session.add(entry_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ChildSavingPlanRepo._entry_map_to_domain(entry_model)

    @staticmethod
    def update_entry(
        entry: ChildSavingAmountEntryDomain,
    ) -> ChildSavingAmountEntryDomain:
        """Given an existing ChildSavingAmountEntryDomain object, update it in the database and return the updated ChildSavingAmountEntryDomain object."""
        # Get child_saving_plan_model from database
        entry_model = db.session.scalar(
            sa.select(ChildSavingAmountEntry).where(
                ChildSavingAmountEntry.id == entry.id
            )
        )
        if not entry_model:
            raise ValueError("ChildSavingAmountEntry not found")

        # Update ChildSavingPlan Model
        entry_model.name = entry.name
        entry_model.start_age = entry.start_age
        entry_model.end_age = entry.end_age
        entry_model.amount = entry.amount
        entry_model.child_saving_plan_id = entry.child_saving_plan_id

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            origin_attr = getattr(entry_model, attr)
            setattr(
                entry_model,
                attr,
                getattr(entry, attr, origin_attr),
            )

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ChildSavingPlanRepo._entry_map_to_domain(entry_model)

    @staticmethod
    def get_entry_by_id(entry_id: str) -> ChildSavingAmountEntryDomain:
        """Retrieve a child_saving_amount_entry by ID and return as DomainObject."""
        # Get child_saving_plan_model from database
        entry_model = db.session.scalar(
            sa.select(ChildSavingAmountEntry).where(
                ChildSavingAmountEntry.id == entry_id
            )
        )
        if not entry_model:
            return None

        # Return the domain object with attributes populated from the database
        return ChildSavingPlanRepo._entry_map_to_domain(entry_model)

    @staticmethod
    def list_entries(child_saving_plan_id: str) -> list[ChildSavingAmountEntryDomain]:
        """Retrieve all child_saving_amount_entries of the plan and return as a list of ChildSavingAmountEntryDomain objects."""
        entry_model_list = db.session.scalars(
            sa.select(ChildSavingAmountEntry).where(
                ChildSavingAmountEntry.child_saving_plan_id == child_saving_plan_id
            )
        ).all()
        return [
            ChildSavingPlanRepo._entry_map_to_domain(entry_model)
            for entry_model in entry_model_list
        ]

    @staticmethod
    def delete_entry_by_id(
        entry_id: str,
    ) -> None:
        """Given an child_saving_amount_entry ID, remove it from the database."""
        # Get child_saving_plan_model from database
        entry_model = db.session.scalar(
            sa.select(ChildSavingAmountEntry).where(
                ChildSavingAmountEntry.id == entry_id
            )
        )
        if entry_model:
            db.session.delete(entry_model)
            db.session.commit()

        return None

    @staticmethod
    def _entry_map_to_domain(
        child_saving_amount_entry: ChildSavingAmountEntry,
    ) -> ChildSavingAmountEntryDomain:
        """Helper method to map the ChildSavingPlan model to a Domain Object."""
        # Get child_saving_amount_entries from database
        return ChildSavingAmountEntryDomain(
            id=child_saving_amount_entry.id,
            child_saving_plan_id=child_saving_amount_entry.child_saving_plan_id,
            name=child_saving_amount_entry.name,
            start_age=child_saving_amount_entry.start_age,
            end_age=child_saving_amount_entry.end_age,
            amount=child_saving_amount_entry.amount,
            created_at=child_saving_amount_entry.created_at,
            updated_at=child_saving_amount_entry.updated_at,
            description=child_saving_amount_entry.description,
        )
