from dataclasses import dataclass, field
from typing import Optional  # , Callable
from datetime import datetime
from abc import ABC  # , abstractmethod
from nanoid import generate


# Every Entity should have id, created_at, and updated_at
@dataclass(kw_only=True)
class EntityDomain(ABC):
    """
    Base domain class for all entities.
    - `id`: immutable identifier generated in domain (e.g., 13-char ULID/UUID)
    - `created_at`, `updated_at`: set by the ORM, not by domain logic
    """

    # Domain-generated ID, once set, id should be read-only
    _id: str = field(default_factory=lambda: generate(size=13))
    # created_at and updated_at is given by orm
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def id(self) -> str:
        return self._id


# Each Resource should have name and description
# Resources could be simulated by year
@dataclass(kw_only=True)
class ResourceDomain(EntityDomain):
    name: str
    description: Optional[str] = None

    def __repr__(self):
        class_name = self.__class__.__name__

        return f"{class_name}(id={self.id}, name={self.name})"

    # @abstractmethod
    # def simulate_by_year(self, simulate_func: Callable):
    #     pass
