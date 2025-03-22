from dataclasses import dataclass
from typing import Optional
from .base import BaseAssociationDomain


@dataclass(kw_only=True)
class ScenarioChildDomain(BaseAssociationDomain):
    birth_age: Optional[int] = None
    independent_age: Optional[int] = None
