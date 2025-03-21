from dataclasses import dataclass
from typing import Optional, Callable
from datetime import datetime
from abc import ABC, abstractmethod


# Every Entity should have id, created_at, and updated_at
@dataclass
class EntityDomain(ABC):
    id: str
    created_at: datetime
    updated_at: datetime


# Each Resource should have name and description
# Resources could be simulated by year
@dataclass
class ResourceDomain(ABC, EntityDomain):
    name: str
    description: Optional[str] = None

    @abstractmethod
    def simulate_by_year(self, simulate_func: Callable):
        pass
