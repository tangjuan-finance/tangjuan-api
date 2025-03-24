from dataclasses import dataclass
from typing import Optional, Callable
from decimal import Decimal
from .base import ResourceRepo
from .account import AccountRepo


@dataclass(kw_only=True)
class HouseRepo(ResourceRepo):
    owner: AccountRepo
    amount: int
    down_payment: int
    interest_rate: Decimal
    loan_term: int
    purchase_age: int
    sale_age: Optional[int] = None

    def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
        return simulate_func(self.amount)
