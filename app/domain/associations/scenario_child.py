from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from .base import BaseAssociationDomain

if TYPE_CHECKING:
    from ..entities import ChildDomain  # Imported only for type hints


@dataclass(kw_only=True)
class ScenarioChildDomain(BaseAssociationDomain):
    child: "ChildDomain"  # Use a forward reference (string)
    birth_age: Optional[int] = None
    independent_age: Optional[int] = None
