from dataclasses import dataclass

from .mixin import BaseAgeIntervalMixin
from .base import ResourceDomain


@dataclass(kw_only=True, repr=False)
class ChildSavingAmountEntryDomain(ResourceDomain, BaseAgeIntervalMixin):
    """
    Represents a saving amount entry at a specific age for a child savings plan.
    """

    amount: int
    child_saving_plan_id: str
