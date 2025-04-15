from dataclasses import dataclass

# from typing import Callable
from decimal import Decimal
from .base import ResourceDomain
from .mixin import BaseAgeIntervalMixin
from .account import AccountDomain


@dataclass(kw_only=True, repr=False)
class IncomeDomain(ResourceDomain, BaseAgeIntervalMixin):
    owner: AccountDomain
    amount: int
    max_yearly_growth_rate: Decimal
    min_yearly_growth_rate: Decimal

    # def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
    #     return simulate_func(self.amount)
    def __repr__(self) -> str:
        return (
            f"IncomeDomain("
            f"id={self.id}, "
            f"owner_id={self.owner.id}, "
            f"amount={self.amount}, "
            f"max_yearly_growth_rate={self.max_yearly_growth_rate}%, "
            f"min_yearly_growth_rate={self.min_yearly_growth_rate}%)"
        )
