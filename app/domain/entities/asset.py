from dataclasses import dataclass
from typing import Callable
from decimal import Decimal
from .base import ResourceDomain
from .mixin import BaseAgeIntervalMixin


@dataclass
class AssetDomain(ResourceDomain, BaseAgeIntervalMixin):
    owner_id: str
    amount: int
    max_yearly_return_rate: Decimal
    min_yearly_return_rate: Decimal

    def simulate_by_year(self, simulate_func: Callable[[Decimal], Decimal]) -> Decimal:
        return simulate_func(self.amount)
