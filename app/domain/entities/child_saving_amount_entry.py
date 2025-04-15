from dataclasses import dataclass
from typing import ClassVar
from .mixin import BaseAgeIntervalMixin
from .base import ResourceDomain


@dataclass(kw_only=True, repr=False)
class ChildSavingAmountEntryDomain(ResourceDomain, BaseAgeIntervalMixin):
    """
    Represents a saving amount entry at a specific age for a child savings plan.
    """

    amount: int
    child_saving_plan_id: str
    _updatable_attrs: ClassVar[set[str]] = {
        "name",
        "start_age",
        "end_age",
        "amount",
        "description",
    }

    def __repr__(self) -> str:
        return (
            f"ChildSavingAmountEntryDomain("
            f"id={self.id}, "
            f"child_saving_plan_id={self.child_saving_plan_id}, "
            f"amount={self.amount})"
        )
