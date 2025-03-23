from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from .base import BaseAssociationDomain
from .mixin import BaseAgeIntervalMixin

if TYPE_CHECKING:
    from ..entities import LiabilityDomain  # Imported only for type hints


@dataclass(kw_only=True)
class ScenarioLiabilityDomain(BaseAssociationDomain, BaseAgeIntervalMixin):
    liability: "LiabilityDomain"  # Use a forward reference (string)
    allocation_percentage: Decimal
    interest_rate: Optional[Decimal]
