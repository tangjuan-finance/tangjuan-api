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
