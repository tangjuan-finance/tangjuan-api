from app.domain.entities import AccountDomain
from app.repository.entities import AccountRepo


class OwnerRequiredServiceMixin:
    """Mixin for services that require ownership validation."""

    @staticmethod
    def _get_owner(owner_id: str) -> AccountDomain:
        """Retrieve the owner account by ID. Raises ValueError if not found."""
        owner = AccountRepo.get_by_id(
            account_id=owner_id,
        )

        if not owner:
            raise ValueError(f"Owner with ID {owner_id} not found")
        return owner
