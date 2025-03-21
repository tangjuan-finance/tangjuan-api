from dataclasses import dataclass
from typing import Callable
from decimal import Decimal
from .base import ResourceDomain


@dataclass
class LiabilityDomain(ResourceDomain):
    owner_id: str
    principal_amount: int
    interest_rate: Decimal
    start_age: int
    end_age: int

    def simulate_by_year(
        self, simulate_func: Callable[[Decimal, Decimal], Decimal]
    ) -> Decimal:
        return simulate_func(self.amount)
