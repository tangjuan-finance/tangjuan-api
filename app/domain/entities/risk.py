from dataclasses import dataclass

# from typing import Callable
from .base import ResourceDomain
from .mixin import BaseAgeIntervalMixin
from .account import AccountDomain
from decimal import Decimal


@dataclass(kw_only=True, repr=False)
class RiskDomain(ResourceDomain, BaseAgeIntervalMixin):
    owner: AccountDomain
    amount: int
    probability: Decimal

    # def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
    #     return simulate_func(self.amount)
    def __repr__(self) -> str:
        return (
            f"RiskDomain("
            f"id={self.id}, "
            f"owner_id={self.owner.id}, "
            f"amount={self.amount}, "
            f"probability={self.probability})"
        )
