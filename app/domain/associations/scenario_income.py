from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from .base import BaseAssociationDomain
from .mixin import BaseAgeIntervalMixin


@dataclass(kw_only=True)
class ScenarioIncomeDomain(BaseAssociationDomain, BaseAgeIntervalMixin):
    income_id: str
    max_yearly_growth_rate: Optional[Decimal] = None
    min_yearly_growth_rate: Optional[Decimal] = None

    def __repr__(self):
        class_name = self.__class__.__name__
        return (
            f"{class_name}(scenario_id={self.scenario_id}, income_id={self.income_id})"
        )
