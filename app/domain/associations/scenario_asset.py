from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from .base import BaseAssociationDomain
from .mixin import BaseAgeIntervalMixin


@dataclass(kw_only=True)
class ScenarioAssetDomain(BaseAssociationDomain, BaseAgeIntervalMixin):
    asset_id: str
    allocation_percentage: Decimal
    max_yearly_return_rate: Optional[Decimal] = None
    min_yearly_return_rate: Optional[Decimal] = None
