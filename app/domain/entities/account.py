from dataclasses import dataclass
from .base import EntityDomain
from datetime import datetime
from typing import Optional


@dataclass(kw_only=True)
class AccountDomain(EntityDomain):
    email: str
    password_hash: str
    name: str
    last_seen: Optional[datetime] = None

    def __repr__(self) -> str:
        return (
            f"AccountDomain("
            f"id={self.id}, "
            f"name={self.name}, "
            f"last_seen={self.last_seen.strftime('%Y-%m-%d %H:%M:%S')})"
        )
