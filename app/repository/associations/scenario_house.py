from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from .base import BaseAssociationRepo

if TYPE_CHECKING:
    from ..entities import HouseRepo  # Imported only for type hints


@dataclass(kw_only=True)
class ScenarioHouseRepo(BaseAssociationRepo):
    house: "HouseRepo"  # Use a forward reference (string)
    down_payment: Optional[int] = None
    interest_rate: Optional[Decimal] = None
    loan_term: Optional[int] = None
    purchase_age: Optional[int] = None
    sale_age: Optional[int] = None
