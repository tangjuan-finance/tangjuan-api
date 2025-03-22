from dataclasses import dataclass
from typing import Optional, Callable
from .base import ResourceDomain


@dataclass(kw_only=True)
class ChildDomain(ResourceDomain):
    parent_id: str
    amount: int
    birth_age: int
    independent_age: Optional[int] = None

    def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
        return simulate_func(self.amount)
