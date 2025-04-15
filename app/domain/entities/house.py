from dataclasses import dataclass

# from typing import Optional, Callable
from decimal import Decimal
from .base import ResourceDomain
from .account import AccountDomain


@dataclass(kw_only=True, repr=False)
class HouseDomain(ResourceDomain):
    owner: AccountDomain
    amount: int
    down_payment: int
    interest_rate: Decimal
    loan_term: int
    purchase_age: int
    sale_age: int

    # def simulate_by_year(self, simulate_func: Callable[[int], int]) -> int:
    #     return simulate_func(self.amount)
    def __repr__(self) -> str:
        return (
            f"HouseDomain("
            f"id={self.id}, "
            f"owner_id={self.owner.id}, "
            f"amount={self.amount}, "
            f"down_payment={self.down_payment}, "
            f"interest_rate={self.interest_rate}%, "
            f"loan_term={self.loan_term}y, "
            f"purchase_age={self.purchase_age}, "
            f"sale_age={self.sale_age})"
        )
