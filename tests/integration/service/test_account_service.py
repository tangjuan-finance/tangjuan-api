# from app.service.account_service import AccountService
# from tests.integration.service.factories import create_account_payload, create_account
# from nanoid import generate
# import pytest


# class TestAccountServiceCase:
#     """Test cases for AccountService."""

#     def test_create_account_service(self):
#         """Test creating an account using AccountService"""

#         # Arrange: Define the expected fields that should be part of the AccountDomain
#         payload = create_account_payload()
#         fields = {
#             "username",
#             "email",
#             "password_hash",
#             "last_seen",
#         }

#         # Act: Call the service to create the account
#         account_domain = AccountService.create_account(payload=payload)

#         # Assert: Ensure the returned AccountDomain matches the input payload
#         for field in fields:
#             # Make sure each field in AccountDomain matches the corresponding payload value
#             assert (
#                 getattr(account_domain, field) == payload[field]
#             ), f"Field {field} does not match expected value."

#     def test_get_account_by_id_service(self):
#         """Test retrieving an account by ID"""

#         # Arrange: Create an account first
#         payload = create_account_payload()
#         account_domain = AccountService.create_account(payload=payload)
#         account_id = account_domain.id

#         # Arrange: Define payload for retrieval
#         get_payload = {
#             "id": account_id,
#         }
#         # Act: Retrieve the account by ID
#         get_account_by_id_domain = AccountService.get_account_by_id(
#             payload=get_payload,
#         )

#         assert get_account_by_id_domain.id == account_id
#         assert get_account_by_id_domain == account_domain

#     def test_update_account_service(self):
#         """Test updating an account using AccountService"""

#         # Arrange: Create an account first
#         payload = create_account_payload()
#         account_domain = AccountService.create_account(payload=payload)
#         account_id = account_domain.id

#         # Arrange: Define updated parameters
#         updated_username = "Updated Account Service"

#         updated_payload = {
#             "id": account_id,
#             "username": updated_username,
#         }

#         # Act: Update account through the service
#         updated_account_domain = AccountService.update_account(
#             payload=updated_payload
#         )

#         # Assert: Ensure the account is updated
#         assert updated_account_domain.id == account_id
#         assert updated_account_domain.username == updated_username

#     def test_delete_account_by_id_service(self):
#         """Test deleting an account by ID"""

#         # Arrange: Create an account first
#         payload = create_account_payload()
#         account_domain = AccountService.create_account(payload=payload)
#         account_id = account_domain.id

#         # Arrange: Define payload for deletion
#         delete_payload = {
#             "id": account_id,
#         }

#         # Act: Delete the account
#         AccountService.delete_account_by_id(
#             payload=delete_payload,
#         )

#         # Assert: Attempt to retrieve the deleted account will fail
#         with pytest.raises(ValueError):
#             AccountService.get_account_by_id(payload=delete_payload)


#     def test_get_account_by_id_service_with_not_existed_account(self):
#         """Test getting a not_existed account"""

#         # Arrange: Generate an account id
#         not_existed_account_id = generate(size=13)

#         # Arrange: Define payload for retrieval
#         get_payload = {
#             "id": not_existed_account_id,
#         }

#         # Assert: Get account with invalid id should fail
#         with pytest.raises(ValueError):
#             AccountService.get_account_by_id(
#                 payload=get_payload,
#             )

#     def test_update_account_service_with_not_existed_account(self):
#         """Test updating a not_existed account"""

#         # Arrange: Generate an account id
#         not_existed_account_id = generate(size=13)

#         # Arrange: Define updated parameters
#         updated_name = "Updated Account Service"

#         updated_payload = {
#             "id": not_existed_account_id,
#             "name": updated_name,
#         }

#         # Assert: Update account with invalid id should fail
#         with pytest.raises(ValueError):
#             AccountService.update_account(
#                 payload=updated_payload
#             )

#     def test_delete_account_service_with_not_existed_account(self):
#         """Test deleting a not_existed account"""

#         # Arrange: Generate an account id
#         not_existed_account_id = generate(size=13)

#         # Arrange: Define payload for retrieval
#         delete_payload = {
#             "id": not_existed_account_id,
#         }

#         # Assert: Delete account with invalid id should fail
#         with pytest.raises(ValueError):
#             AccountService.delete_account_by_id(
#                 payload=delete_payload
#             )

#     def test_create_account_service_with_invalid_field(self):
#         """Test creating an account with invalid field using AccountService"""

#         # Arrange: Given parameters for account creation
#         payload = create_account_payload()

#         # Arrange: Add an invalid field
#         invalid_field_name = "invalid_field"
#         payload[invalid_field_name] = "this field is invalid"

#         # Arrange: Given parameters for account creation
#         account_domain = AccountService.create_account(payload=payload)

#         # Assert: The invalid field is not added
#         assert hasattr(account_domain, invalid_field_name) is False

#     def test_update_account_service_with_invalid_field(self):
#         """Test updating an account with invalid field using AccountService"""

#         # Arrange: Given parameters for account creation
#         payload = create_account_payload()

#         # Arrange: Given parameters for account creation
#         account_domain = AccountService.create_account(payload=payload)
#         account_id = account_domain.id

#         # Arrange: Define updated parameters
#         updated_username = "Updated Account Service"

#         updated_payload = {
#             "id": account_id,
#             "username": updated_username,
#         }

#         # Arrange: Add an invalid field
#         invalid_field_name = "invalid_field"
#         updated_payload[invalid_field_name] = "this field is invalid"

#         # Act: Retrieve the account by ID
#         updated_account = AccountService.update_account(
#             payload=updated_payload
#         )

#         assert hasattr(updated_account, invalid_field_name) is False

#     def test_create_account_service_miss_required_field(self):
#         """Test creating an account using AccountService"""
#         # Arrange: Define the expected fields that should be part of the AccountDomain
#         payload = create_account_payload()

#         # Arrange: Remove required field
#         del payload["username"]

#         # Assert: Create account when missing required field should raise ValueError
#         with pytest.raises(ValueError):
#             AccountService.create_account(payload=payload)
