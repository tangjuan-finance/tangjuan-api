from dataclasses import dataclass

# from typing import Callable
from decimal import Decimal
from .base import ResourceDomain
from .mixin import BaseAgeIntervalMixin
from .account import AccountDomain


@dataclass(kw_only=True, repr=False)
class ExpenseDomain(ResourceDomain, BaseAgeIntervalMixin):
    owner: AccountDomain
    amount: int
    max_yearly_growth_rate: Decimal
    min_yearly_growth_rate: Decimal

    # def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
    #     return simulate_func(self.amount)
