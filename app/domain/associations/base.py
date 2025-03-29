from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from abc import ABC

if TYPE_CHECKING:
    from ..entities import ScenarioDomain  # Imported only for type hints


# Every Association should have scenario_id, created_at, and updated_at
@dataclass(kw_only=True)
class BaseAssociationDomain(ABC):
    scenario: "ScenarioDomain"  # Use a forward reference (string)
    memo: Optional[str] = None
    # created_at and updated_at is given by orm
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
