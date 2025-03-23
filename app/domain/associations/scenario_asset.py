from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from .base import BaseAssociationDomain
from .mixin import BaseAgeIntervalMixin

if TYPE_CHECKING:
    from ..entities import AssetDomain  # Imported only for type hints


@dataclass(kw_only=True)
class ScenarioAssetDomain(BaseAssociationDomain, BaseAgeIntervalMixin):
    asset: "AssetDomain"  # Use a forward reference (string)
    allocation_percentage: Decimal
    max_yearly_return_rate: Optional[Decimal] = None
    min_yearly_return_rate: Optional[Decimal] = None
