from dataclasses import dataclass
from typing import Optional, Callable
from .base import ResourceDomain
from .mixin import BaseAgeIntervalMixin


@dataclass
class RiskDomain(ResourceDomain, BaseAgeIntervalMixin):
    owner_id: str
    max_loss: int
    min_loss: int
    start_age: int
    end_age: Optional[int]

    def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
        return simulate_func(self.amount)
