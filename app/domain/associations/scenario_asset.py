from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from .base import BaseAssociationDomain
from .mixin import BaseAgeIntervalMixin


@dataclass(kw_only=True)
class ScenarioAssetDomain(BaseAssociationDomain, BaseAgeIntervalMixin):
    owner_id: str
    amount: int
    max_yearly_return_rate: Optional[Decimal] = None
    min_yearly_return_rate: Optional[Decimal] = None
