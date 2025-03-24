from dataclasses import dataclass
from typing import Callable
from decimal import Decimal
from .base import ResourceRepo
from .mixin import BaseAgeIntervalMixin
from .account import AccountRepo


@dataclass(kw_only=True)
class IncomeRepo(ResourceRepo, BaseAgeIntervalMixin):
    owner: AccountRepo
    amount: int
    max_yearly_growth_rate: Decimal
    min_yearly_growth_rate: Decimal

    def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
        return simulate_func(self.amount)
