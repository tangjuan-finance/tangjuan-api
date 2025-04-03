from app.service.associations import ScenarioRiskService
from app.domain.entities import RiskDomain

from .factories import create_scenario_risk_payload
from tests.factory import create_risk, create_account

from nanoid import generate
import pytest


class TestScenarioRiskServiceCase:
    """Test cases for ScenarioRiskService."""

    def test_create_scenario_risk_service(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test creating an assoc using ScenarioRiskService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=default_risk_id
        )

        # Act: Call the service to create the assoc
        response = ScenarioRiskService.create_scenario_risk(
            account_id=account_id, payload=payload
        )

        assoc, risk = response.get("association"), response.get("risk")

        # Assert: Ensure the returned assoc matches the input payload
        for field in payload.keys():
            # Make sure each field in the assoc matches the corresponding payload value
            assert (
                getattr(assoc, field) == payload[field]
            ), f"Field {field} does not match expected value."

        # Assert: Check the return risk is the same as the given risk
        assert isinstance(risk, RiskDomain)
        assert risk.id == default_risk_id

    def test_get_risk_service_by_id(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test retrieving an assoc by ID using ScenarioRiskService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=default_risk_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioRiskService.create_scenario_risk(account_id=account_id, payload=payload)

        # Arrange: Define payload for retrieval
        get_payload = {
            "scenario_id": default_scenario_id,
            "risk_id": default_risk_id,
        }

        # Act: Retrieve the risk by ID
        response = ScenarioRiskService.get_scenario_risk_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assoc, risk = response.get("association"), response.get("risk")

        # Assert: Check cid of assoc is as given
        assert assoc.scenario_id == default_scenario_id
        assert assoc.risk_id == default_risk_id

        # Assert: Check id of risk is as given
        assert risk.id == default_risk_id

    def test_get_risks_service(self, default_account, default_scenario_id):
        """Test retrieving a list of Scenario Risk Assoc using ScenarioRiskService"""

        # Arrange: Get the initial count of risks
        account_id = default_account.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "scenario_id": default_scenario_id,
        }

        original_assocs_count = len(
            ScenarioRiskService.get_scenario_risks(
                account_id=account_id, payload=get_payload
            )
        )

        # Arrange: Create multiple assocs
        new_assoc_count = 5
        created_assocs = [
            ScenarioRiskService.create_scenario_risk(
                account_id,
                create_scenario_risk_payload(
                    scenario_id=default_scenario_id,
                    risk_id=create_risk(default_account).id,
                ),
            ).get("association")
            for _ in range(new_assoc_count)
        ]
        # Act: Retrieve updated list of assocs
        assocs_from_service = [
            response["association"]
            for response in ScenarioRiskService.get_scenario_risks(
                account_id=account_id, payload=get_payload
            )
        ]
        updated_assocs_count = len(assocs_from_service)

        # Assert: Ensure each created risk exists in the retrieved list
        assert all(assoc in assocs_from_service for assoc in created_assocs)

        # Assert: Ensure the total count has increased by the created number
        assert updated_assocs_count == original_assocs_count + new_assoc_count

    def test_update_scenario_risk_service(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test updating an assoc using ScenarioRiskService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=default_risk_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioRiskService.create_scenario_risk(account_id=account_id, payload=payload)

        # Arrange: Define updated parameters
        updated_memo = "Updated Assoc Memo"

        updated_payload = {
            "scenario_id": default_scenario_id,
            "risk_id": default_risk_id,
            "memo": updated_memo,
        }

        # Act: Update assoc through the service
        response = ScenarioRiskService.update_scenario_risk(
            account_id=account_id, payload=updated_payload
        )
        assoc = response.get("association")

        # Assert: Ensure the assoc is updated
        assert assoc.scenario_id == default_scenario_id
        assert assoc.risk_id == default_risk_id
        assert assoc.memo == updated_memo

    def test_delete_risk_service_by_id(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test deleting an assoc by ID using ScenarioRiskService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=default_risk_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioRiskService.create_scenario_risk(account_id=account_id, payload=payload)

        # Arrange: Define payload for deletion
        delete_payload = {
            "scenario_id": default_scenario_id,
            "risk_id": default_risk_id,
        }

        # Act: Delete the risk
        ScenarioRiskService.delete_scenario_risk_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted risk will fail
        with pytest.raises(ValueError):
            ScenarioRiskService.get_scenario_risk_by_id(
                account_id=account_id, payload=delete_payload
            )

    def test_create_scenario_risk_service_when_owner_account_not_match(
        self, default_scenario_id, default_risk_id
    ):
        """Test creating an assoc using ScenarioRiskService when resource owner and account are not match"""

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=default_risk_id
        )

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Act: Call the service to create the assoc with a different account should raise Permission Error
        with pytest.raises(PermissionError):
            ScenarioRiskService.create_scenario_risk(
                account_id=another_account_id, payload=payload
            )

    def test_get_risk_service_by_id_when_owner_account_not_match(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test retrieving an assoc by ID using ScenarioRiskService when resource owner and account are not match"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=default_risk_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioRiskService.create_scenario_risk(account_id=account_id, payload=payload)

        # Arrange: Define payload for retrieval
        get_payload = {
            "scenario_id": default_scenario_id,
            "risk_id": default_risk_id,
        }

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Act: Call the service to retrieve the assoc with a different account should raise Permission Error
        with pytest.raises(PermissionError):
            ScenarioRiskService.get_scenario_risk_by_id(
                account_id=another_account_id, payload=get_payload
            )

    def test_get_risks_service_when_owner_account_not_match(
        self, default_account, default_scenario_id
    ):
        """Test retrieving a list of Scenario Risk Assoc using ScenarioRiskService when resource owner and account are not match"""

        # Arrange: Get the initial count of risks
        account_id = default_account.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "scenario_id": default_scenario_id,
        }

        # Arrange: Create multiple assocs
        new_assoc_count = 5
        [
            ScenarioRiskService.create_scenario_risk(
                account_id,
                create_scenario_risk_payload(
                    scenario_id=default_scenario_id,
                    risk_id=create_risk(default_account).id,
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
                for response in ScenarioRiskService.get_scenario_risks(
                    account_id=another_account_id, payload=get_payload
                )
            ]

    def test_update_risk_service_by_id_when_owner_account_not_match(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test updating an assoc by ID using ScenarioRiskService when resource owner and account are not match"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=default_risk_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioRiskService.create_scenario_risk(account_id=account_id, payload=payload)

        # Arrange: Define updated parameters
        updated_memo = "Updated Assoc Memo"
        updated_payload = {
            "scenario_id": default_scenario_id,
            "risk_id": default_risk_id,
            "memo": updated_memo,
        }

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Act: Call the service to update the assoc with a different account should raise Permission Error
        with pytest.raises(PermissionError):
            ScenarioRiskService.update_scenario_risk(
                account_id=another_account_id, payload=updated_payload
            )

    def test_delete_scenario_risk_service_when_owner_account_not_match(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test deleting an assoc using ScenarioRiskService when resource owner and account are not match"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=default_risk_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioRiskService.create_scenario_risk(account_id=account_id, payload=payload)

        # Arrange: Define payload for retrieval
        delete_payload = {
            "scenario_id": default_scenario_id,
            "risk_id": default_risk_id,
        }

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Act: Call the service to retrieve the assoc with a different account should raise Permission Error
        with pytest.raises(PermissionError):
            ScenarioRiskService.delete_scenario_risk_by_id(
                account_id=another_account_id, payload=delete_payload
            )

    def test_create_scenario_risk_service_when_non_existed_resource(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test creating an assoc by ID using ScenarioRiskService with not existed resource"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Generate not existed scenario_id
        non_existed_scenario_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=non_existed_scenario_id, risk_id=default_risk_id
        )

        # Act: Call the service to create the assoc with a different account should raise Permission Error
        with pytest.raises(ValueError):
            ScenarioRiskService.create_scenario_risk(
                account_id=account_id, payload=payload
            )

        # Arrange: Generate not existed scenario_id
        non_existed_risk_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=non_existed_risk_id
        )

        # Act: Call the service to create the assoc with a different account should raise Permission Error
        with pytest.raises(ValueError):
            ScenarioRiskService.create_scenario_risk(
                account_id=account_id, payload=payload
            )

    def test_get_risk_service_by_id_with_non_existed_resource(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test retrieving an assoc by ID using ScenarioRiskService with not existed resource"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Generate not existed scenario_id
        non_existed_scenario_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        get_payload = {
            "scenario_id": non_existed_scenario_id,
            "risk_id": default_risk_id,
        }

        # Arrange: Call the service to create the assoc with non_existed scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioRiskService.get_scenario_risk_by_id(
                account_id=account_id, payload=get_payload
            )

        # Arrange: Generate not existed risk_id
        non_existed_risk_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        get_payload = {
            "scenario_id": default_scenario_id,
            "risk_id": non_existed_risk_id,
        }

        # Arrange: Call the service to create the assoc with non_existed scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioRiskService.get_scenario_risk_by_id(
                account_id=account_id, payload=get_payload
            )

    def test_update_risk_service_by_id_with_non_existed_resource(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test updating an assoc by ID using ScenarioRiskService with not existed resource"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Generate not existed scenario_id
        non_existed_scenario_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_memo = "Updated Assoc Memo"
        updated_payload = {
            "scenario_id": non_existed_scenario_id,
            "risk_id": default_risk_id,
            "memo": updated_memo,
        }

        # Act: Call the service to update the assoc of non-existed scenario should raise Permission Error
        with pytest.raises(ValueError):
            ScenarioRiskService.update_scenario_risk(
                account_id=account_id, payload=updated_payload
            )

        # Arrange: Generate not existed risk_id
        non_existed_risk_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_memo = "Updated Assoc Memo"
        updated_payload = {
            "scenario_id": default_scenario_id,
            "risk_id": non_existed_risk_id,
            "memo": updated_memo,
        }

        # Act: Call the service to update the assoc of non-existed scenario should raise Permission Error
        with pytest.raises(ValueError):
            ScenarioRiskService.update_scenario_risk(
                account_id=account_id, payload=updated_payload
            )

    def test_delete_risk_service_by_id_with_non_existed_resource(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test deleting an assoc by ID using ScenarioRiskService with not existed resource"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Generate not existed scenario_id
        non_existed_scenario_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        delete_payload = {
            "scenario_id": non_existed_scenario_id,
            "risk_id": default_risk_id,
        }

        # Arrange: Call the service to delete the assoc with non_existed scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioRiskService.delete_scenario_risk_by_id(
                account_id=account_id, payload=delete_payload
            )

        # Arrange: Generate not existed risk_id
        non_existed_risk_id = generate(size=13)

        # Arrange: Create the expected fields in the payload
        delete_payload = {
            "scenario_id": default_scenario_id,
            "risk_id": non_existed_risk_id,
        }

        # Arrange: Call the service to delete the assoc with non_existed scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioRiskService.delete_scenario_risk_by_id(
                account_id=account_id, payload=delete_payload
            )

    def test_create_scenario_risk_service_with_invalid_field(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test creating an assoc using ScenarioRiskService with invalid field"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=default_risk_id
        )

        # Arrange: Create invalid field
        payload["invalid_field"] = "this is an invalid field"

        # Act: Call the service to create the assoc with invalid field should raise TypeError
        with pytest.raises(TypeError):
            ScenarioRiskService.create_scenario_risk(
                account_id=account_id, payload=payload
            )

    def test_update_risk_service_by_id_with_invalid_field(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test updating an assoc by ID using ScenarioRiskService with invalid field"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=default_risk_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioRiskService.create_scenario_risk(account_id=account_id, payload=payload)

        # Arrange: Define updated parameters
        updated_memo = "Updated Assoc Memo"
        updated_payload = {
            "scenario_id": default_scenario_id,
            "risk_id": default_risk_id,
            "memo": updated_memo,
        }

        # Arrange: Create invalid field
        invalid_filed_name = "invalid_field"
        updated_payload[invalid_filed_name] = "this is an invalid field"

        # Act: Call the service to update the assoc
        response = ScenarioRiskService.update_scenario_risk(
            account_id=account_id, payload=updated_payload
        )

        assoc = response.get("association")

        # Assoc should not contain invalid field
        with pytest.raises(AttributeError):
            getattr(assoc, invalid_filed_name)

    def test_create_scenario_risk_service_with_invalid_cid(
        self, default_account, default_scenario_id, default_risk_id
    ):
        """Test creating an assoc using ScenarioRiskService with invalid cid"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_risk_payload(
            scenario_id=default_scenario_id, risk_id=default_risk_id
        )

        # Act: Modified scenario_id to invalid str
        payload["scenario_id"] = "this is an invalid scenario_id"

        # Act: Call the service to create the assoc with invalid cid should raise TypeError
        with pytest.raises(ValueError):
            ScenarioRiskService.create_scenario_risk(
                account_id=account_id, payload=payload
            )

        # Act: Modified scenario_id to invalid datatype
        payload["scenario_id"] = 103284

        # Act: Call the service to create the assoc with invalid cid should raise TypeError
        with pytest.raises(TypeError):
            ScenarioRiskService.create_scenario_risk(
                account_id=account_id, payload=payload
            )
