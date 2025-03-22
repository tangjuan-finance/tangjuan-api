from dataclasses import dataclass
from typing import Callable
from .base import ResourceDomain
from .mixin import BaseAgeIntervalMixin
from .account import AccountDomain


@dataclass(kw_only=True)
class RiskDomain(ResourceDomain, BaseAgeIntervalMixin):
    owner: AccountDomain
    max_loss: int
    min_loss: int

    def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
        return simulate_func(self.amount)
