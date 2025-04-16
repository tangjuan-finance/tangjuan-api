from dataclasses import dataclass, field

from .base import ResourceDomain
from .child_saving_amount_entry import ChildSavingAmountEntryDomain
from typing import Optional, Any


@dataclass(kw_only=True, repr=False)
class ChildSavingPlanDomain(ResourceDomain):
    """
    Represents a child saving plan that contains a sequence of saving amount entries.
    """

    independent_age: int
    owner_id: str
    child_saving_amount_entries: list[ChildSavingAmountEntryDomain] = field(
        default_factory=list
    )

    def __repr__(self) -> str:
        return (
            f"ChildSavingPlanDomain("
            f"id={self.id}, "
            f"owner_id={self.owner_id}, "
            f"independent_age={self.independent_age}, "
            f"entries={len(self.child_saving_amount_entries)})"
        )

    def add_entry(
        self,
        name: str,
        start_age: int,
        end_age: int,
        amount: int,
        description: Optional[str] = None,
    ) -> ChildSavingAmountEntryDomain:
        """Create a new entry and attach it to the plan."""
        # Create the entry based on the given attr
        new_entry = ChildSavingAmountEntryDomain(
            name=name,
            child_saving_plan_id=self.id,
            start_age=start_age,
            end_age=end_age,
            amount=amount,
            description=description,
        )

        # Add the entry to the object
        self.child_saving_amount_entries.append(new_entry)

        return new_entry

    def get_entry_by_id(self, entry_id: str) -> Optional[ChildSavingAmountEntryDomain]:
        """Return entry by ID or None if not found."""
        return next(
            (
                entry
                for entry in self.child_saving_amount_entries
                if entry.id == entry_id
            ),
            None,
        )

    def list_entries(
        self,
    ) -> list[ChildSavingAmountEntryDomain]:
        """Return a shallow copy of the entry list to prevent external mutation."""
        # return copy to avoid mutation
        return list(self.child_saving_amount_entries)

    def update_entry_by_id(
        self,
        entry_id: str,
        **kwargs: Any,
    ) -> Optional[ChildSavingAmountEntryDomain]:
        """
        Update entry attributes by ID. Raises ValueError if not found.
        Only updates known attributes.
        """
        entry = self.get_entry_by_id(entry_id)
        if not entry:
            raise ValueError(f"Entry with id {entry_id} not found.")

        unknown_fields = set(kwargs.keys()) - entry._updatable_attrs
        if unknown_fields:
            raise ValueError(f"Unknown fields: {unknown_fields}")

        for attr_name, attr_value in kwargs.items():
            if attr_name in entry._updatable_attrs:
                setattr(entry, attr_name, attr_value)

        return entry

    def remove_entry_by_id(self, entry_id: str) -> None:
        """
        Remove an entry from the plan by ID.
        Raises ValueError if not found.
        """
        entry = self.get_entry_by_id(entry_id=entry_id)
        if not entry:
            raise ValueError(f"Entry with id {entry_id} not found.")

        self.child_saving_amount_entries.remove(entry)
