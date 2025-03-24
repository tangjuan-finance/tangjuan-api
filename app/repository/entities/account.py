from dataclasses import dataclass
from .base import EntityRepo
from datetime import datetime


@dataclass(kw_only=True)
class AccountRepo(EntityRepo):
    username: str
    email: str
    password_hash: str
    last_seen: datetime
