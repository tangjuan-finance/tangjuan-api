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

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(scenario_id={self.scenario_id}, asset_id={self.asset_id})"
