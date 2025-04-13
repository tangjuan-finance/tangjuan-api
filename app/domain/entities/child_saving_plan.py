from dataclasses import dataclass, field

from .base import ResourceDomain
from .child_saving_amount_entry import ChildSavingAmountEntryDomain


@dataclass(kw_only=True)
class ChildSavingPlanDomain(ResourceDomain):
    """
    Represents a child saving plan that contains a sequence of saving amount entries.
    """

    owner_id: str
    child_saving_amount_entries: list[ChildSavingAmountEntryDomain] = field(
        default_factory=list
    )
