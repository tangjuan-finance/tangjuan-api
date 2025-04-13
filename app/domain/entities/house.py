from dataclasses import dataclass
from typing import Optional  # , Callable
from decimal import Decimal
from .base import ResourceDomain
from .account import AccountDomain


@dataclass(kw_only=True)
class HouseDomain(ResourceDomain):
    owner: AccountDomain
    amount: int
    down_payment: int
    interest_rate: Decimal
    loan_term: int
    purchase_age: int
    sale_age: Optional[int] = None

    # def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
    #     return simulate_func(self.amount)
