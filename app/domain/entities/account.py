from dataclasses import dataclass
from .base import EntityDomain
from datetime import datetime


@dataclass(kw_only=True)
class AccountDomain(EntityDomain):
    username: str
    email: str
    password_hash: str
    last_seen: datetime
