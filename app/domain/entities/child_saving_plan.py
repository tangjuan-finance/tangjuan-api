from dataclasses import dataclass, field

from .base import ResourceDomain
from .child_saving_amount_entry import ChildSavingAmountEntryDomain
from typing import Optional


@dataclass(kw_only=True)
class ChildSavingPlanDomain(ResourceDomain):
    """
    Represents a child saving plan that contains a sequence of saving amount entries.
    """

    independent_age: int
    owner_id: str
    child_saving_amount_entries: list[ChildSavingAmountEntryDomain] = field(
        default_factory=list
    )

    def add_entry(
        self,
        name: str,
        start_age: int,
        end_age: int,
        amount: int,
        description: Optional[str] = None,
    ):  # -> None:
        # Domain rule validation
        if start_age > end_age:
            raise ValueError(
                f"start_age should less than end_age, get {start_age} > {end_age} instead"
            )

        if not self.id:
            raise ValueError("Should save this plan to database first to get plan id.")

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
        # self.child_saving_amount_entries.append(new_entry)

        # return None
        return new_entry

    def update_entry(
        entry_id: str,
        name: Optional[str] = None,
        start_age: Optional[int] = None,
        end_age: Optional[int] = None,
        amount: Optional[int] = None,
        description: Optional[str] = None,
    ):
        pass

    def remove_entry(entry_id: str):
        pass

    def get_entry(entry_id: str):
        pass

    def list_entries():
        pass
