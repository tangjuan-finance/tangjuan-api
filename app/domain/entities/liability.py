from dataclasses import dataclass
from typing import Callable
from decimal import Decimal
from .base import ResourceDomain
from .account import AccountDomain


@dataclass(kw_only=True)
class LiabilityDomain(ResourceDomain):
    owner: AccountDomain
    principal_amount: int
    interest_rate: Decimal
    start_age: int
    end_age: int

    def simulate_by_year(self, simulate_func: Callable[[int, int], int]) -> int:
        return simulate_func(self.amount)
