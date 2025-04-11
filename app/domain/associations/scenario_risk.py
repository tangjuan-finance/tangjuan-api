from dataclasses import dataclass
from typing import Optional
from .base import BaseAssociationDomain
from .mixin import BaseAgeIntervalMixin
from decimal import Decimal


@dataclass(kw_only=True)
class ScenarioRiskDomain(BaseAssociationDomain, BaseAgeIntervalMixin):
    risk_id: str
    probability: Optional[Decimal] = None
