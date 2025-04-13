from dataclasses import dataclass
from typing import Optional

from .base import EntityDomain


@dataclass(kw_only=True)
class ChildSavingAmountEntryDomain(EntityDomain):
    """
    Represents a saving amount entry at a specific age for a child savings plan.
    """

    age: int
    amount: int
    child_saving_plan_id: str
    description: Optional[str] = None
