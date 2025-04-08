from abc import ABC, abstractmethod
from app.domain.associations import BaseAssociationDomain


# Repo class for all entity
class AssociationRepo(ABC):
    @staticmethod
    @abstractmethod
    def create(*args, **kwargs) -> BaseAssociationDomain:
        """Create and return the corresponding association."""
        pass

    @staticmethod
    @abstractmethod
    def save(*args, **kwargs) -> BaseAssociationDomain:
        """Save and return the corresponding association."""
        pass

    @staticmethod
    @abstractmethod
    def get_by_id(*args, **kwargs) -> BaseAssociationDomain | None:
        """Return association by ID or None if not found."""
        pass

    @staticmethod
    @abstractmethod
    def get_list(*args, **kwargs) -> list[BaseAssociationDomain]:
        """Return a list of associations owned by the same account.
        Or empty list if no instance founded
        """
        pass

    @staticmethod
    @abstractmethod
    def delete_by_id(*args, **kwargs) -> None:
        """Delete the association by ID."""
        pass

    @staticmethod
    @abstractmethod
    def _map_to_domain(*args, **kwargs) -> BaseAssociationDomain:
        """Map ORM model to association."""
        pass
