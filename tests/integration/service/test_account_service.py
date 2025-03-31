from app.service.account_service import AccountService
from tests.integration.service.factories import create_account_payload, create_account
from nanoid import generate
import pytest
from werkzeug.security import generate_password_hash, check_password_hash


class TestAccountServiceCase:
    """Test cases for AccountService."""

    def test_create_account_service(self):
        """Test creating an account using AccountService"""

        # Arrange: Define the expected fields that should be part of the AccountDomain
        payload = create_account_payload()
        fields = {
            "name",
            "email",
        }

        # Act: Call the service to create the account
        account_domain = AccountService.create_account(payload=payload)

        # Assert: Ensure the returned AccountDomain matches the input payload
        for field in fields:
            # Make sure each field in AccountDomain matches the corresponding payload value
            assert (
                getattr(account_domain, field) == payload[field]
            ), f"Field {field} does not match expected value."

        assert check_password_hash(account_domain.password_hash, payload["password"])

    def test_get_account_by_id_service(self):
        """Test retrieving an account by ID"""

        # Arrange: Create an account first
        payload = create_account_payload()
        account_domain = AccountService.create_account(payload=payload)
        account_id = account_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": account_id,
        }
        # Act: Retrieve the account by ID
        get_account_by_id_domain = AccountService.get_account_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assert get_account_by_id_domain.id == account_id
        assert get_account_by_id_domain == account_domain

    def test_update_account_service(self):
        """Test updating an account using AccountService"""

        # Arrange: Create an account first
        payload = create_account_payload()
        account_domain = AccountService.create_account(payload=payload)
        account_id = account_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Account Service"

        updated_payload = {
            "id": account_id,
            "name": updated_name,
        }

        # Act: Update account through the service
        updated_account_domain = AccountService.update_account(
            account_id=account_id, payload=updated_payload
        )

        # Assert: Ensure the account is updated
        assert updated_account_domain.id == account_id
        assert updated_account_domain.name == updated_name

    def test_delete_account_by_id_service(self):
        """Test deleting an account by ID"""

        # Arrange: Create an account first
        payload = create_account_payload()
        account_domain = AccountService.create_account(payload=payload)
        account_id = account_domain.id

        # Arrange: Define payload for deletion
        delete_payload = {
            "id": account_id,
        }

        # Act: Delete the account
        AccountService.delete_account_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted account will fail
        with pytest.raises(ValueError):
            AccountService.get_account_by_id(
                account_id=account_id, payload=delete_payload
            )

    def test_get_account_by_id_service_user_account_not_match(self, default_account):
        """Test getting an account when user and account are not match"""

        # Arrange: Create an account first
        account_id = default_account.id
        payload = create_account_payload()
        new_account_domain = AccountService.create_account(payload=payload)
        another_account_id = new_account_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": another_account_id,
        }

        with pytest.raises(PermissionError):
            AccountService.get_account_by_id(
                account_id=account_id,
                payload=get_payload,
            )

    def test_update_account_service_user_account_not_match(self, default_account):
        """Test updating an account when user and account are not match"""

        # Arrange: Create an account first
        account_id = default_account.id
        payload = create_account_payload()
        new_account_domain = AccountService.create_account(payload=payload)
        another_account_id = new_account_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Account Service"

        updated_payload = {
            "id": another_account_id,
            "name": updated_name,
        }

        # Act: Retrieve the account by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            AccountService.update_account(
                account_id=account_id, payload=updated_payload
            )

    def test_delete_account_service_user_account_not_match(self, default_account):
        """Test deleting an account when user and account are not match"""

        # Arrange: Create an account first
        account_id = default_account.id
        payload = create_account_payload()
        new_account_domain = AccountService.create_account(payload=payload)
        another_account_id = new_account_domain.id

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": another_account_id,
        }

        with pytest.raises(PermissionError):
            AccountService.delete_account_by_id(
                account_id=account_id, payload=delete_payload
            )

    def test_get_account_by_id_service_with_not_existed_account(self, default_account):
        """Test getting a not existed account by a not existed account"""

        # Arrange: Generate an account id
        not_existed_account_id = generate(size=13)

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": not_existed_account_id,
        }

        # Assert: Get account with invalid id should fail
        with pytest.raises(ValueError):
            AccountService.get_account_by_id(
                account_id=not_existed_account_id,
                payload=get_payload,
            )

    def test_update_account_service_with_not_existed_account(self):
        """Test updating a not existed account by a not existed account"""

        # Arrange: Generate an account id
        not_existed_account_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_name = "Updated Account Service"

        updated_payload = {
            "id": not_existed_account_id,
            "name": updated_name,
        }

        # Assert: Update account with invalid id should fail
        with pytest.raises(ValueError):
            AccountService.update_account(
                account_id=not_existed_account_id,
                payload=updated_payload,
            )

    def test_delete_account_service_with_not_existed_account(self):
        """Test deleting a not existed account by a not existed account"""

        # Arrange: Generate an account id
        not_existed_account_id = generate(size=13)

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": not_existed_account_id,
        }

        # Assert: Delete account with invalid id should fail
        with pytest.raises(ValueError):
            AccountService.delete_account_by_id(
                account_id=not_existed_account_id, payload=delete_payload
            )

    def test_create_account_service_with_invalid_field(self):
        """Test creating an account with invalid field using AccountService"""

        # Arrange: Given parameters for account creation
        payload = create_account_payload()

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        payload[invalid_field_name] = "this field is invalid"

        # Arrange: Given parameters for account creation
        account_domain = AccountService.create_account(payload=payload)

        # Assert: The invalid field is not added
        assert hasattr(account_domain, invalid_field_name) is False

    def test_update_account_service_with_invalid_field(self):
        """Test updating an account with invalid field using AccountService"""

        # Arrange: Given parameters for account creation
        payload = create_account_payload()

        # Arrange: Given parameters for account creation
        account_domain = AccountService.create_account(payload=payload)
        account_id = account_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Account Service"

        updated_payload = {
            "id": account_id,
            "name": updated_name,
        }

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        updated_payload[invalid_field_name] = "this field is invalid"

        # Act: Retrieve the account by ID
        updated_account = AccountService.update_account(
            account_id=account_id, payload=updated_payload
        )

        assert hasattr(updated_account, invalid_field_name) is False

    def test_create_account_service_miss_required_field(self):
        """Test creating an account using AccountService while missing required fields"""
        # Arrange: Define the expected fields that should be part of the AccountDomain
        payload = create_account_payload()

        # Arrange: Remove required field
        del payload["name"]

        # Assert: Create account when missing required field should raise ValueError
        with pytest.raises(ValueError):
            AccountService.create_account(payload=payload)

    def test_create_account_service_without_email(self):
        """Test creating an account without email using AccountService"""
        # Arrange: Define the expected fields that should be part of the AccountDomain
        payload = create_account_payload()

        # Arrange: Remove required field
        del payload["email"]

        # Assert: Create account when missing required field should raise ValueError
        with pytest.raises(ValueError):
            AccountService.create_account(payload=payload)

    def test_create_account_service_without_password(self):
        """Test creating an account without password using AccountService"""
        # Arrange: Define the expected fields that should be part of the AccountDomain
        payload = create_account_payload()

        # Arrange: Remove required field
        del payload["password"]

        # Assert: Create account when missing required field should raise ValueError
        with pytest.raises(ValueError):
            AccountService.create_account(payload=payload)

    def test_update_account_service_for_changing_email(self):
        """Test changing email in account directly using AccountService"""

        # Arrange: Given parameters for account creation
        payload = create_account_payload()

        # Arrange: Given parameters for account creation
        account_domain = AccountService.create_account(payload=payload)
        account_id = account_domain.id

        # Arrange: Changing email
        updated_email = "updateemailshouldfail.myemail.com"

        updated_payload = {
            "id": account_id,
            "email": updated_email,
        }

        # Assert: Changing email directly should raise ValueError
        with pytest.raises(ValueError):
            AccountService.update_account(
                account_id=account_id, payload=updated_payload
            )

    def test_update_account_service_with_password_hash(self):
        """Test updating password of account by directly providing password_hash using AccountService"""

        # Arrange: Given parameters for account creation
        payload = create_account_payload()

        # Arrange: Given parameters for account creation
        account_domain = AccountService.create_account(payload=payload)
        account_id = account_domain.id

        # Arrange: Changing email
        updated_password = "this_is_update_pa44word"
        updated_password_hash = generate_password_hash(updated_password)

        updated_payload = {
            "id": account_id,
            "password_hash": updated_password_hash,
        }

        # Act: Attempt to update account
        updated_account_domain = AccountService.update_account(
            account_id=account_id, payload=updated_payload
        )
        # Assert: Password should remain unchanged
        assert (
            check_password_hash(updated_account_domain.password_hash, updated_password)
            is False
        )
