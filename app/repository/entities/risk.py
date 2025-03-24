from dataclasses import dataclass
from typing import Callable
from .base import ResourceRepo
from .mixin import BaseAgeIntervalMixin
from .account import AccountRepo


@dataclass(kw_only=True)
class RiskRepo(ResourceRepo, BaseAgeIntervalMixin):
    owner: AccountRepo
    max_loss: int
    min_loss: int

    def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
        return simulate_func(self.amount)
