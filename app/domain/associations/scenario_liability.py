from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from .base import BaseAssociationDomain
from .mixin import BaseAgeIntervalMixin


@dataclass(kw_only=True)
class ScenarioLiabilityDomain(BaseAssociationDomain, BaseAgeIntervalMixin):
    interest_rate: Optional[Decimal]
