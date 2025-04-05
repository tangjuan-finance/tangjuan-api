from abc import ABC


class CheckOwnershipMixin(ABC):
    def _check_ownership_by_id(account_id: str, owner_id: str):
        # Check if the account owns the entity
        if owner_id != account_id:
            raise PermissionError(f"Account {account_id} does not own this entity")
