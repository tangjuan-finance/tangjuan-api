from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from abc import ABC


# Every Association should have scenario_id, created_at, and updated_at
@dataclass(kw_only=True)
class BaseAssociationDomain(ABC):
    scenario_id: str
    memo: Optional[str] = None
    # created_at and updated_at is given by orm
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
