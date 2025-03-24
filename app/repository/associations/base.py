from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from abc import ABC

if TYPE_CHECKING:
    from ..entities import ScenarioRepo  # Imported only for type hints


# Every Association should have scenario_id, created_at, and updated_at
@dataclass(kw_only=True)
class BaseAssociationRepo(ABC):
    scenario: "ScenarioRepo"  # Use a forward reference (string)
    memo: Optional[str] = None
    created_at: datetime
    updated_at: datetime
