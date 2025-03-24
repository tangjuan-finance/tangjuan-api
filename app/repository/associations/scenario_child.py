from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from .base import BaseAssociationRepo

if TYPE_CHECKING:
    from ..entities import ChildRepo  # Imported only for type hints


@dataclass(kw_only=True)
class ScenarioChildRepo(BaseAssociationRepo):
    child: "ChildRepo"  # Use a forward reference (string)
    birth_age: Optional[int] = None
    independent_age: Optional[int] = None
