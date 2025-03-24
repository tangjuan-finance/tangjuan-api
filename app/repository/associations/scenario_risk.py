from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from .base import BaseAssociationRepo
from .mixin import BaseAgeIntervalMixin

if TYPE_CHECKING:
    from ..entities import RiskRepo  # Imported only for type hints


@dataclass(kw_only=True)
class ScenarioRiskRepo(BaseAssociationRepo, BaseAgeIntervalMixin):
    risk: "RiskRepo"  # Use a forward reference (string)
    max_loss: Optional[int] = None
    min_loss: Optional[int] = None
