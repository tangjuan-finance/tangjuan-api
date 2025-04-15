from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from .base import EntityDomain
from .account import AccountDomain


@dataclass(kw_only=True, repr=False)
class ScenarioDomain(EntityDomain):
    owner: "AccountDomain"
    name: str
    asset_allocation_percentage: Decimal
    retire_age: int
    description: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"ScenarioDomain("
            f"id={self.id}, "
            f"owner_id={self.owner.id}, "
            f"name={self.name}, "
            f"asset_allocation_percentage={self.asset_allocation_percentage}, "
            f"retire_age={self.retire_age})"
        )
