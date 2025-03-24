from dataclasses import dataclass
from typing import Callable
from decimal import Decimal
from .base import ResourceRepo
from .account import AccountRepo


@dataclass(kw_only=True)
class LiabilityRepo(ResourceRepo):
    owner: AccountRepo
    principal_amount: int
    interest_rate: Decimal
    start_age: int
    end_age: int

    def simulate_by_year(self, simulate_func: Callable[[int, int], int]) -> int:
        return simulate_func(self.amount)
