from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from .base import BaseAssociationDomain
from .mixin import BaseAgeIntervalMixin

if TYPE_CHECKING:
    from ..entities import RiskDomain  # Imported only for type hints


@dataclass(kw_only=True)
class ScenarioRiskDomain(BaseAssociationDomain, BaseAgeIntervalMixin):
    risk: "RiskDomain"  # Use a forward reference (string)
    max_loss: Optional[int] = None
    min_loss: Optional[int] = None
