from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from .base import EntityDomain


@dataclass
class ScenarioDomain(EntityDomain):
    owner_id: str
    name: str
    description: Optional[str] = None
    asset_allocation_percentage: Decimal
    retire_age: int
