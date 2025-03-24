from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from .base import BaseAssociationRepo
from .mixin import BaseAgeIntervalMixin

if TYPE_CHECKING:
    from ..entities import LiabilityRepo  # Imported only for type hints


@dataclass(kw_only=True)
class ScenarioLiabilityRepo(BaseAssociationRepo, BaseAgeIntervalMixin):
    liability: "LiabilityRepo"  # Use a forward reference (string)
    allocation_percentage: Decimal
    interest_rate: Optional[Decimal] = None
