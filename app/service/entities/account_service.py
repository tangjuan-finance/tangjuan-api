from app.domain.entities import AccountDomain
from app.repository.entities import AccountRepo
from werkzeug.security import generate_password_hash


class AccountService:
    # Fields required during creation
    _required_fields = {
        "name",
        "email",
        "password",
    }
    _all_fields = _required_fields | {
        "last_seen",
    }

    # Fields that can be updated (mutable)
    _immutable_fields = {"email"}

    @staticmethod
    def create_account(payload: dict) -> AccountDomain:
        """Create a new account."""

        # Validate required fields
        missing_fields = AccountService._required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Handle password hashing and exclude it from the payload to avoid saving plain text password
        password = payload.get("password")
        if password:
            password_hash = generate_password_hash(password)
        else:
            raise ValueError("Password is required")

        # Filter payload to include only allowed fields and exclude plain password
        account_payload = {
            field: payload[field]
            for field in AccountService._all_fields
            if field in payload and field != "password"  # Prevent saving plain password
        }

        # Add hashed password to account payload
        account_payload["password_hash"] = password_hash

        # Create the account
        account = AccountDomain(**account_payload)
        return AccountRepo.create(account)

    @staticmethod
    def get_account_by_id(account_id: str, payload: dict) -> AccountDomain:
        """Retrieve a specific account by ID."""
        target_account_id = payload.get("id")
        if not target_account_id:
            raise ValueError("Account ID is required")

        # Check if the target account is the same as the user account
        if account_id != target_account_id:
            raise PermissionError(f"Account {account_id} does not own this resource")

        account_from_repo = AccountRepo.get_by_id(target_account_id)
        if not account_from_repo:
            raise ValueError(f"Account with ID {target_account_id} not found")

        return account_from_repo

    @staticmethod
    def update_account(account_id: str, payload: dict) -> AccountDomain:
        """Update an account by ID if it exists."""

        # Fetch the account to update
        account_from_repo = AccountService.get_account_by_id(
            account_id=account_id, payload=payload
        )

        for field in AccountService._all_fields:
            if field in payload:
                if field in AccountService._immutable_fields:
                    raise ValueError(f"Field {field} is immutable.")
                elif field == "password":
                    # Update password hash
                    updated_password_hash = generate_password_hash(payload[field])
                    setattr(account_from_repo, "password_hash", updated_password_hash)
                else:
                    # Update other fields
                    setattr(account_from_repo, field, payload[field])

        # Save the updated account
        return AccountRepo.save(account_from_repo)

    @staticmethod
    def delete_account_by_id(account_id: str, payload: dict) -> str:
        """Delete an account by ID if it exists."""
        account = AccountService.get_account_by_id(
            account_id=account_id, payload=payload
        )  # Raises if not found
        AccountRepo.delete_by_id(account.id)
        return f"Account {account.id} deleted successfully"
