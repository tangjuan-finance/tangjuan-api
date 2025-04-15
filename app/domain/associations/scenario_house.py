from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from .base import BaseAssociationDomain


@dataclass(kw_only=True)
class ScenarioHouseDomain(BaseAssociationDomain):
    house_id: str
    down_payment: Optional[int] = None
    interest_rate: Optional[Decimal] = None
    loan_term: Optional[int] = None
    purchase_age: Optional[int] = None
    sale_age: Optional[int] = None

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(scenario_id={self.scenario_id}, house_id={self.house_id})"
