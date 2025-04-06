from abc import ABC, abstractmethod
from app.domain.entities import EntityDomain


# Repo class for all entity
class EntityRepo(ABC):
    @staticmethod
    @abstractmethod
    def create(*args, **kwargs) -> EntityDomain:
        """Create and return the corresponding domain entity."""
        pass

    @staticmethod
    @abstractmethod
    def save(*args, **kwargs) -> EntityDomain:
        """Save and return the corresponding domain entity."""
        pass

    @staticmethod
    @abstractmethod
    def get_by_id(*args, **kwargs) -> EntityDomain | None:
        """Return domain entity by ID or None if not found."""
        pass

    @staticmethod
    @abstractmethod
    def get_list(*args, **kwargs) -> list[EntityDomain]:
        """Return a list of domain entities owned by the same account.
        Or empty list if no instance founded
        """
        pass

    @staticmethod
    @abstractmethod
    def delete_by_id(*args, **kwargs) -> None:
        """Delete the entity by ID."""
        pass

    @staticmethod
    @abstractmethod
    def _map_to_domain(*args, **kwargs) -> EntityDomain:
        """Map ORM model to domain entity."""
        pass


# Repo for all entity except account
class ResourceRepo(EntityRepo):
    """Repo base class for domain resources (non-account entities)."""

    pass
