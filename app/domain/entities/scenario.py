from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from .base import EntityDomain


@dataclass(kw_only=True)
class ScenarioDomain(EntityDomain):
    owner_id: str
    name: str
    asset_allocation_percentage: Decimal
    retire_age: int
    description: Optional[str] = None
