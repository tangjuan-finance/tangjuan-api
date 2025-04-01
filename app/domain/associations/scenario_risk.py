from dataclasses import dataclass
from typing import Optional
from .base import BaseAssociationDomain
from .mixin import BaseAgeIntervalMixin


@dataclass(kw_only=True)
class ScenarioRiskDomain(BaseAssociationDomain, BaseAgeIntervalMixin):
    risk_id: str
    max_loss: Optional[int] = None
    min_loss: Optional[int] = None
