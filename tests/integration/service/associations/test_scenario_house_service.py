from app.service.associations import ScenarioHouseService
from app.domain.entities import HouseDomain

from .factories import create_scenario_house_payload
from tests.factory import create_house, create_account

from nanoid import generate
import pytest


class TestScenarioHouseServiceCase:
    """Test cases for ScenarioHouseService."""

    def test_create_scenario_house_service(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test creating an assoc using ScenarioHouseService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=default_house_id
        )

        # Act: Call the service to create the assoc
        response = ScenarioHouseService.create_scenario_house(
            account_id=account_id, payload=payload
        )

        assoc, house = response.get("association"), response.get("house")

        # Assert: Ensure the returned assoc matches the input payload
        for field in payload.keys():
            # Make sure each field in the assoc matches the corresponding payload value
            assert (
                getattr(assoc, field) == payload[field]
            ), f"Field {field} does not match expected value."

        # Assert: Check the return house is the same as the given house
        assert isinstance(house, HouseDomain)
        assert house.id == default_house_id

    def test_get_house_service_by_id(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test retrieving an assoc by ID using ScenarioHouseService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=default_house_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioHouseService.create_scenario_house(
            account_id=account_id, payload=payload
        )

        # Arrange: Define payload for retrieval
        get_payload = {
            "scenario_id": default_scenario_id,
            "house_id": default_house_id,
        }

        # Act: Retrieve the house by ID
        response = ScenarioHouseService.get_scenario_house_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assoc, house = response.get("association"), response.get("house")

        # Assert: Check cid of assoc is as given
        assert assoc.scenario_id == default_scenario_id
        assert assoc.house_id == default_house_id

        # Assert: Check id of house is as given
        assert house.id == default_house_id

    def test_get_houses_service(self, default_account, default_scenario_id):
        """Test retrieving a list of Scenario House Assoc using ScenarioHouseService"""

        # Arrange: Get the initial count of houses
        account_id = default_account.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "scenario_id": default_scenario_id,
        }

        original_assocs_count = len(
            ScenarioHouseService.get_scenario_houses(
                account_id=account_id, payload=get_payload
            )
        )

        # Arrange: Create multiple assocs
        new_assoc_count = 5
        created_assocs = [
            ScenarioHouseService.create_scenario_house(
                account_id,
                create_scenario_house_payload(
                    scenario_id=default_scenario_id,
                    house_id=create_house(default_account).id,
                ),
            ).get("association")
            for _ in range(new_assoc_count)
        ]
        # Act: Retrieve updated list of assocs
        assocs_from_service = [
            response["association"]
            for response in ScenarioHouseService.get_scenario_houses(
                account_id=account_id, payload=get_payload
            )
        ]
        updated_assocs_count = len(assocs_from_service)

        # Assert: Ensure each created house exists in the retrieved list
        assert all(assoc in assocs_from_service for assoc in created_assocs)

        # Assert: Ensure the total count has increased by the created number
        assert updated_assocs_count == original_assocs_count + new_assoc_count

    def test_update_scenario_house_service(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test updating an assoc using ScenarioHouseService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=default_house_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioHouseService.create_scenario_house(
            account_id=account_id, payload=payload
        )

        # Arrange: Define updated parameters
        updated_memo = "Updated Assoc Memo"

        updated_payload = {
            "scenario_id": default_scenario_id,
            "house_id": default_house_id,
            "memo": updated_memo,
        }

        # Act: Update assoc through the service
        response = ScenarioHouseService.update_scenario_house(
            account_id=account_id, payload=updated_payload
        )
        assoc = response.get("association")

        # Assert: Ensure the assoc is updated
        assert assoc.scenario_id == default_scenario_id
        assert assoc.house_id == default_house_id
        assert assoc.memo == updated_memo

    def test_delete_house_service_by_id(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test deleting an assoc by ID using ScenarioHouseService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=default_house_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioHouseService.create_scenario_house(
            account_id=account_id, payload=payload
        )

        # Arrange: Define payload for deletion
        delete_payload = {
            "scenario_id": default_scenario_id,
            "house_id": default_house_id,
        }

        # Act: Delete the house
        ScenarioHouseService.delete_scenario_house_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted house will fail
        with pytest.raises(ValueError):
            ScenarioHouseService.get_scenario_house_by_id(
                account_id=account_id, payload=delete_payload
            )

    def test_create_scenario_house_service_when_owner_account_not_match(
        self, default_scenario_id, default_house_id
    ):
        """Test creating an assoc using ScenarioHouseService when resource owner and account are not match"""

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=default_house_id
        )

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Act: Call the service to create the assoc with a different account should raise Permission Error
        with pytest.raises(PermissionError):
            ScenarioHouseService.create_scenario_house(
                account_id=another_account_id, payload=payload
            )

    def test_get_house_service_by_id_when_owner_account_not_match(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test retrieving an assoc by ID using ScenarioHouseService when resource owner and account are not match"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=default_house_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioHouseService.create_scenario_house(
            account_id=account_id, payload=payload
        )

        # Arrange: Define payload for retrieval
        get_payload = {
            "scenario_id": default_scenario_id,
            "house_id": default_house_id,
        }

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Act: Call the service to retrieve the assoc with a different account should raise Permission Error
        with pytest.raises(PermissionError):
            ScenarioHouseService.get_scenario_house_by_id(
                account_id=another_account_id, payload=get_payload
            )

    def test_get_houses_service_when_owner_account_not_match(
        self, default_account, default_scenario_id
    ):
        """Test retrieving a list of Scenario House Assoc using ScenarioHouseService when resource owner and account are not match"""

        # Arrange: Get the initial count of houses
        account_id = default_account.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "scenario_id": default_scenario_id,
        }

        # Arrange: Create multiple assocs
        new_assoc_count = 5
        [
            ScenarioHouseService.create_scenario_house(
                account_id,
                create_scenario_house_payload(
                    scenario_id=default_scenario_id,
                    house_id=create_house(default_account).id,
                ),
            ).get("association")
            for _ in range(new_assoc_count)
        ]

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Act: Retrieve updated list of assocs with a different account should raise Permission Error
        # As there is no assoc in this fresh created account
        with pytest.raises(PermissionError):
            [
                response["association"]
                for response in ScenarioHouseService.get_scenario_houses(
                    account_id=another_account_id, payload=get_payload
                )
            ]

    def test_update_house_service_by_id_when_owner_account_not_match(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test updating an assoc by ID using ScenarioHouseService when resource owner and account are not match"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=default_house_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioHouseService.create_scenario_house(
            account_id=account_id, payload=payload
        )

        # Arrange: Define updated parameters
        updated_memo = "Updated Assoc Memo"
        updated_payload = {
            "scenario_id": default_scenario_id,
            "house_id": default_house_id,
            "memo": updated_memo,
        }

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Act: Call the service to update the assoc with a different account should raise Permission Error
        with pytest.raises(PermissionError):
            ScenarioHouseService.update_scenario_house(
                account_id=another_account_id, payload=updated_payload
            )

    def test_delete_scenario_house_service_when_owner_account_not_match(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test deleting an assoc using ScenarioHouseService when resource owner and account are not match"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=default_house_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioHouseService.create_scenario_house(
            account_id=account_id, payload=payload
        )

        # Arrange: Define payload for retrieval
        delete_payload = {
            "scenario_id": default_scenario_id,
            "house_id": default_house_id,
        }

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Act: Call the service to retrieve the assoc with a different account should raise Permission Error
        with pytest.raises(PermissionError):
            ScenarioHouseService.delete_scenario_house_by_id(
                account_id=another_account_id, payload=delete_payload
            )

    def test_create_scenario_house_service_when_non_existed_resource(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test creating an assoc by ID using ScenarioHouseService with not existed resource"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Generate not existed scenario_id
        non_existed_scenario_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=non_existed_scenario_id, house_id=default_house_id
        )

        # Act: Call the service to create the assoc with a different account should raise Permission Error
        with pytest.raises(ValueError):
            ScenarioHouseService.create_scenario_house(
                account_id=account_id, payload=payload
            )

        # Arrange: Generate not existed scenario_id
        non_existed_house_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=non_existed_house_id
        )

        # Act: Call the service to create the assoc with a different account should raise Permission Error
        with pytest.raises(ValueError):
            ScenarioHouseService.create_scenario_house(
                account_id=account_id, payload=payload
            )

    def test_get_house_service_by_id_with_non_existed_resource(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test retrieving an assoc by ID using ScenarioHouseService with not existed resource"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Generate not existed scenario_id
        non_existed_scenario_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        get_payload = {
            "scenario_id": non_existed_scenario_id,
            "house_id": default_house_id,
        }

        # Arrange: Call the service to create the assoc with non_existed scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioHouseService.get_scenario_house_by_id(
                account_id=account_id, payload=get_payload
            )

        # Arrange: Generate not existed house_id
        non_existed_house_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        get_payload = {
            "scenario_id": default_scenario_id,
            "house_id": non_existed_house_id,
        }

        # Arrange: Call the service to create the assoc with non_existed scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioHouseService.get_scenario_house_by_id(
                account_id=account_id, payload=get_payload
            )

    def test_update_house_service_by_id_with_non_existed_resource(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test updating an assoc by ID using ScenarioHouseService with not existed resource"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Generate not existed scenario_id
        non_existed_scenario_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_memo = "Updated Assoc Memo"
        updated_payload = {
            "scenario_id": non_existed_scenario_id,
            "house_id": default_house_id,
            "memo": updated_memo,
        }

        # Act: Call the service to update the assoc of non-existed scenario should raise Permission Error
        with pytest.raises(ValueError):
            ScenarioHouseService.update_scenario_house(
                account_id=account_id, payload=updated_payload
            )

        # Arrange: Generate not existed house_id
        non_existed_house_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_memo = "Updated Assoc Memo"
        updated_payload = {
            "scenario_id": default_scenario_id,
            "house_id": non_existed_house_id,
            "memo": updated_memo,
        }

        # Act: Call the service to update the assoc of non-existed scenario should raise Permission Error
        with pytest.raises(ValueError):
            ScenarioHouseService.update_scenario_house(
                account_id=account_id, payload=updated_payload
            )

    def test_delete_house_service_by_id_with_non_existed_resource(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test deleting an assoc by ID using ScenarioHouseService with not existed resource"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Generate not existed scenario_id
        non_existed_scenario_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        delete_payload = {
            "scenario_id": non_existed_scenario_id,
            "house_id": default_house_id,
        }

        # Arrange: Call the service to delete the assoc with non_existed scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioHouseService.delete_scenario_house_by_id(
                account_id=account_id, payload=delete_payload
            )

        # Arrange: Generate not existed house_id
        non_existed_house_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        delete_payload = {
            "scenario_id": default_scenario_id,
            "house_id": non_existed_house_id,
        }

        # Arrange: Call the service to delete the assoc with non_existed scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioHouseService.delete_scenario_house_by_id(
                account_id=account_id, payload=delete_payload
            )

    def test_create_scenario_house_service_with_invalid_field(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test creating an assoc using ScenarioHouseService with invalid field"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=default_house_id
        )

        # Arrange: Create invalid field
        payload["invalid_field"] = "this is an invalid field"

        # Act: Call the service to create the assoc with invalid field should raise TypeError
        with pytest.raises(TypeError):
            ScenarioHouseService.create_scenario_house(
                account_id=account_id, payload=payload
            )

    def test_update_house_service_by_id_with_invalid_field(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test updating an assoc by ID using ScenarioHouseService with invalid field"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=default_house_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioHouseService.create_scenario_house(
            account_id=account_id, payload=payload
        )

        # Arrange: Define updated parameters
        updated_memo = "Updated Assoc Memo"
        updated_payload = {
            "scenario_id": default_scenario_id,
            "house_id": default_house_id,
            "memo": updated_memo,
        }

        # Arrange: Create invalid field
        invalid_filed_name = "invalid_field"
        updated_payload[invalid_filed_name] = "this is an invalid field"

        # Act: Call the service to update the assoc
        response = ScenarioHouseService.update_scenario_house(
            account_id=account_id, payload=updated_payload
        )

        assoc = response.get("association")

        # Assoc should not contain invalid field
        with pytest.raises(AttributeError):
            getattr(assoc, invalid_filed_name)

    def test_create_scenario_house_service_with_invalid_cid(
        self, default_account, default_scenario_id, default_house_id
    ):
        """Test creating an assoc using ScenarioHouseService with invalid cid"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_house_payload(
            scenario_id=default_scenario_id, house_id=default_house_id
        )

        # Act: Modified scenario_id to invalid str
        payload["scenario_id"] = "this is an invalid scenario_id"

        # Act: Call the service to create the assoc with invalid cid should raise TypeError
        with pytest.raises(ValueError):
            ScenarioHouseService.create_scenario_house(
                account_id=account_id, payload=payload
            )

        # Act: Modified scenario_id to invalid datatype
        payload["scenario_id"] = 103284

        # Act: Call the service to create the assoc with invalid cid should raise TypeError
        with pytest.raises(TypeError):
            ScenarioHouseService.create_scenario_house(
                account_id=account_id, payload=payload
            )
