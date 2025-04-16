from app.domain.entities import ChildSavingPlanDomain, ChildSavingAmountEntryDomain
from app.infrastructure.models import ChildSavingPlan, ChildSavingAmountEntry, Account
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
            owner_id=child_saving_plan.owner_id,
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

        # Get the owner from the database
        owner = db.session.scalar(
            sa.select(Account).where(Account.id == child_saving_plan.owner_id)
        )
        if not owner:
            raise ValueError(f"Account with id {child_saving_plan.owner_id} not found")

        child_saving_plan_model.owner_id = child_saving_plan.owner_id

        # Map the entry from domain to model
        ChildSavingPlanRepo._update_entry_list(
            domain=child_saving_plan, model=child_saving_plan_model
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
    def _update_entry_list(
        domain: ChildSavingPlanDomain, model: ChildSavingPlan
    ) -> None:
        """
        Synchronize the model's child_saving_amount_entries with the domain's entries.
        Supports create, update, and delete using direct list mutation.
        """
        # Get reference of the list for entries in model
        existing_entries = model.child_saving_amount_entries

        # Build dicts for fast access by ID
        existing_entry_dict = {entry.id: entry for entry in existing_entries}
        updating_entry_dict = {
            entry.id: entry for entry in domain.child_saving_amount_entries
        }

        # CREATE or UPDATE
        for entry_id, entry in updating_entry_dict.items():
            # UPDATE: If the update entry exist in the database
            if entry_id in existing_entry_dict:
                # UPDATE: update fields in-place
                existing_entry = existing_entry_dict[entry_id]

                existing_entry.name = entry.name
                existing_entry.start_age = entry.start_age
                existing_entry.end_age = entry.end_age
                existing_entry.amount = entry.amount
                existing_entry.updated_at = entry.updated_at
                existing_entry.description = entry.description
            else:
                # CREATE: append new entry
                new_entry = ChildSavingAmountEntry(
                    id=entry.id,
                    child_saving_plan_id=entry.child_saving_plan_id,
                    name=entry.name,
                    start_age=entry.start_age,
                    end_age=entry.end_age,
                    amount=entry.amount,
                    description=entry.description,
                )
                existing_entries.append(new_entry)

        # DELETE: remove entries not present in the domain
        remove_entry_ids = set(existing_entry_dict.keys()) - set(
            updating_entry_dict.keys()
        )
        for entry_id in remove_entry_ids:
            entry_to_remove = existing_entry_dict[entry_id]
            existing_entries.remove(entry_to_remove)

    @staticmethod
    def _map_to_domain(
        child_saving_plan_model: ChildSavingPlan,
    ) -> ChildSavingPlanDomain:
        """Helper method to map the ChildSavingPlan model to a Domain Object."""
        # Get child_saving_amount_entries from database
        entry_domain_list = [
            ChildSavingPlanRepo._entry_map_to_domain(entry)
            for entry in child_saving_plan_model.child_saving_amount_entries
        ]

        return ChildSavingPlanDomain(
            _id=child_saving_plan_model.id,
            owner_id=child_saving_plan_model.owner_id,
            name=child_saving_plan_model.name,
            independent_age=child_saving_plan_model.independent_age,
            created_at=child_saving_plan_model.created_at,
            updated_at=child_saving_plan_model.updated_at,
            description=child_saving_plan_model.description,
            child_saving_amount_entries=entry_domain_list,
        )

    @staticmethod
    def _entry_map_to_domain(
        child_saving_amount_entry: ChildSavingAmountEntry,
    ) -> ChildSavingAmountEntryDomain:
        """Helper method to map the ChildSavingPlan model to a Domain Object."""
        # Get child_saving_amount_entries from database
        return ChildSavingAmountEntryDomain(
            _id=child_saving_amount_entry.id,
            child_saving_plan_id=child_saving_amount_entry.child_saving_plan_id,
            name=child_saving_amount_entry.name,
            start_age=child_saving_amount_entry.start_age,
            end_age=child_saving_amount_entry.end_age,
            amount=child_saving_amount_entry.amount,
            created_at=child_saving_amount_entry.created_at,
            updated_at=child_saving_amount_entry.updated_at,
            description=child_saving_amount_entry.description,
        )
