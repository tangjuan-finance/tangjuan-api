from app.domain.entities import ResourceDomain


class CheckOwnershipMixin:
    @classmethod
    def _check_ownership_by_id(cls, account_id: str, owner_id: str):
        # Check if the account owns the entity
        if owner_id != account_id:
            raise PermissionError(f"Account {account_id} does not own this entity")

    @classmethod
    def _check_ownership(cls, account_id: str, entity: ResourceDomain):
        # Check if the account owns the entity

        # Get owner ID from either parent or directly
        owner_id = entity.parent.id if hasattr(entity, "parent") else entity.owner.id

        return cls._check_ownership_by_id(account_id, owner_id)
