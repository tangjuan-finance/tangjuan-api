from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from .base import BaseAssociationDomain
from .mixin import BaseAgeIntervalMixin


@dataclass(kw_only=True)
class ScenarioIncomeDomain(BaseAssociationDomain, BaseAgeIntervalMixin):
    max_yearly_growth_rate: Optional[Decimal] = None
    min_yearly_growth_rate: Optional[Decimal] = None
