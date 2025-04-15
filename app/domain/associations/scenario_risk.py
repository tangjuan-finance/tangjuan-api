from dataclasses import dataclass
from typing import Optional
from .base import BaseAssociationDomain
from .mixin import BaseAgeIntervalMixin
from decimal import Decimal


@dataclass(kw_only=True)
class ScenarioRiskDomain(BaseAssociationDomain, BaseAgeIntervalMixin):
    risk_id: str
    probability: Optional[Decimal] = None

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(scenario_id={self.scenario_id}, risk_id={self.risk_id})"
