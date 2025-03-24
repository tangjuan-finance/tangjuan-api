from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from .base import BaseAssociationRepo
from .mixin import BaseAgeIntervalMixin

if TYPE_CHECKING:
    from ..entities import IncomeRepo  # Imported only for type hints


@dataclass(kw_only=True)
class ScenarioIncomeRepo(BaseAssociationRepo, BaseAgeIntervalMixin):
    income: "IncomeRepo"  # Use a forward reference (string)
    max_yearly_growth_rate: Optional[Decimal] = None
    min_yearly_growth_rate: Optional[Decimal] = None
