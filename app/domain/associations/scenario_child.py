from dataclasses import dataclass
from typing import Optional
from .base import BaseAssociationDomain


@dataclass(kw_only=True)
class ScenarioChildDomain(BaseAssociationDomain):
    child_id: str
    birth_age: Optional[int] = None
    independent_age: Optional[int] = None

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(scenario_id={self.scenario_id}, child_id={self.child_id})"
