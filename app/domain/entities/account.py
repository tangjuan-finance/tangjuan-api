from dataclasses import dataclass
from .base import EntityDomain
from datetime import datetime
from typing import Optional


@dataclass(kw_only=True)
class AccountDomain(EntityDomain):
    username: str
    email: str
    password_hash: str
    last_seen: Optional[datetime] = None
