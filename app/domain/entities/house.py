from dataclasses import dataclass
from typing import Optional, Callable
from decimal import Decimal
from .base import ResourceDomain


@dataclass
class HouseDomain(ResourceDomain):
    owner_id: str
    amount: int
    down_payment: int
    interest_rate: Decimal
    loan_term: int
    purchase_age: int
    sale_age: Optional[int]

    def simulate_by_year(self, simulate_func: Callable[[Decimal], Decimal]) -> Decimal:
        return simulate_func(self.amount)
