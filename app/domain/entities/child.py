from dataclasses import dataclass
from typing import Optional, Callable
from .base import ResourceDomain
from .account import AccountDomain


@dataclass(kw_only=True)
class ChildDomain(ResourceDomain):
    parent: AccountDomain
    birth_age: int
    independent_age: Optional[int] = None

    def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
        return simulate_func(self.amount)
