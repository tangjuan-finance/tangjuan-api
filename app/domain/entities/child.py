from dataclasses import dataclass
from typing import Optional, Callable
from decimal import Decimal
from .base import ResourceDomain


@dataclass
class ChildDomain(ResourceDomain):
    parent_id: str
    amount: int
    birth_age: int
    independent_age: Optional[int]

    def simulate_by_year(self, simulate_func: Callable[[Decimal], Decimal]) -> Decimal:
        return simulate_func(self.amount)
