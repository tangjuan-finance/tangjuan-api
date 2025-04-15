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
