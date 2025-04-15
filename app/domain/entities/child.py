from dataclasses import dataclass

# from typing import Callable
from .base import ResourceDomain
from .account import AccountDomain


@dataclass(kw_only=True, repr=False)
class ChildDomain(ResourceDomain):
    """
    Represents a child entity tied to an account and a savings plan.
    """

    parent: AccountDomain
    child_saving_plan_id: str
    birth_age: int

    # def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
    #     return simulate_func(self.amount)
    def __repr__(self) -> str:
        return (
            f"ChildDomain("
            f"id={self.id}, "
            f"parent_id={self.parent.id}, "
            f"child_saving_plan_id={self.child_saving_plan_id}, "
            f"birth_age={self.birth_age})"
        )
