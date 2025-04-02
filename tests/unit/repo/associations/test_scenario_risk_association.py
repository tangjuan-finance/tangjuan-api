from app.repository.associations import ScenarioRiskRepo
from app.infrastructure.models.associations import ScenarioRisk
from app.domain.associations import ScenarioRiskDomain
import sqlalchemy as sa
from app import db

from tests.unit.repo.factories import create_risk, create_scenario
from nanoid import generate
import pytest


class TestRiskRepoCase:
    @staticmethod
    def _create_assoc(risk_id, scenario_id):
        assoc_domain = ScenarioRiskDomain(
            risk_id=risk_id,
            scenario_id=scenario_id,
        )
        return ScenarioRiskRepo.create(assoc_domain)

    def test_create_scenario_risk_assoc_through_repo(self, new_scenario, new_risk):
        # Arrange: Create an risk and a scenario domain using the factory
        default_max_loss = 100000
        new_risk.max_loss = default_max_loss
        assoc_max_loss = 500000

        # Create Assoc Domain
        assoc_domain = ScenarioRiskDomain(
            risk_id=new_risk.id,
            scenario_id=new_scenario.id,
            max_loss=assoc_max_loss,
        )

        # Act: Save the risk domain to the scenario domain by ScenarioRiskRepo, and get the association obj back from database
        scenario_risk_from_repo = ScenarioRiskRepo.create(assoc_domain)

        scenario_risk_from_db = db.session.scalars(
            sa.select(ScenarioRisk).where(
                (ScenarioRisk.scenario_id == scenario_risk_from_repo.scenario_id)
                & (ScenarioRisk.risk_id == scenario_risk_from_repo.risk_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_risk_from_repo.risk_id == scenario_risk_from_db.risk_id
        assert scenario_risk_from_repo.scenario_id == scenario_risk_from_db.scenario_id
        assert scenario_risk_from_repo.max_loss == scenario_risk_from_db.max_loss
        assert scenario_risk_from_repo.max_loss == assoc_max_loss

    def test_update_scenario_risk_assoc_through_repo(self, new_scenario, new_risk):
        # Arrange: Adding a risk to scenario using the ScenarioRiskRepo
        default_max_loss = 500000
        assoc_domain = ScenarioRiskDomain(
            risk_id=new_risk.id,
            scenario_id=new_scenario.id,
            max_loss=default_max_loss,
        )
        scenario_risk_from_repo = ScenarioRiskRepo.create(assoc_domain)
        updated_max_loss = 100000

        # Act: Update the risk domain object (before saving)
        scenario_risk_from_repo.max_loss = updated_max_loss

        # Save the updated object through the repository and get the result
        updated_scenario_risk = ScenarioRiskRepo.save(scenario_risk_from_repo)

        # Query the database to verify the updated risk record
        scenario_risk_from_db = db.session.scalars(
            sa.select(ScenarioRisk).where(
                (ScenarioRisk.scenario_id == scenario_risk_from_repo.scenario_id)
                & (ScenarioRisk.risk_id == scenario_risk_from_repo.risk_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_scenario_risk.risk_id == scenario_risk_from_db.risk_id
        assert updated_scenario_risk.scenario_id == scenario_risk_from_db.scenario_id
        assert updated_scenario_risk.max_loss == updated_max_loss
        assert updated_scenario_risk.max_loss == scenario_risk_from_db.max_loss
        assert updated_scenario_risk.created_at == scenario_risk_from_db.created_at
        assert updated_scenario_risk.updated_at == scenario_risk_from_db.updated_at
        # Update_at from updated_risk should be different from the previous risk domain (the one before update)
        assert updated_scenario_risk.updated_at > scenario_risk_from_repo.updated_at

    def test_get_scenario_risk_assoc_by_id_through_repo(self, new_scenario, new_risk):
        # Arrange: Create an risk domain using the factory
        scenario_risk_from_repo = self._create_assoc(
            risk_id=new_risk.id,
            scenario_id=new_scenario.id,
        )

        # Act: Update the risk domain object (before saving)
        scenario_risk_get_by_id = ScenarioRiskRepo.get_by_id(
            scenario_id=scenario_risk_from_repo.scenario_id,
            risk_id=scenario_risk_from_repo.risk_id,
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert (
            scenario_risk_get_by_id.scenario_id == scenario_risk_from_repo.scenario_id
        )
        assert scenario_risk_get_by_id.risk_id == scenario_risk_from_repo.risk_id

    def test_get_scenario_risk_assoc_list_through_repo(
        self, default_account, new_scenario
    ):
        # Arrange: Create an risk domain using the factory
        origin_repo_list_length = len(
            ScenarioRiskRepo.get_list(scenario_id=new_scenario.id)
        )

        # Act: Create 5 new risk domains
        for _ in range(5):
            new_risk = create_risk(default_account)
            self._create_assoc(
                risk_id=new_risk.id,
                scenario_id=new_scenario.id,
            )

        # Assert: Ensure the list length is increased by 5
        updated_list_length = len(
            ScenarioRiskRepo.get_list(scenario_id=new_scenario.id)
        )
        assert updated_list_length == (origin_repo_list_length + 5)

    def test_delete_scenario_risk_assoc_through_repo(self, new_scenario, new_risk):
        # Arrange: Create an risk domain using the factory
        scenario_risk_from_repo = self._create_assoc(
            risk_id=new_risk.id,
            scenario_id=new_scenario.id,
        )

        # Act: Delete the risk domain object
        ScenarioRiskRepo.delete_by_id(
            scenario_id=scenario_risk_from_repo.scenario_id,
            risk_id=scenario_risk_from_repo.risk_id,
        )

        # Assert: Ensure the risk record is deleted from the database
        scenario_risk_from_db = db.session.scalar(
            sa.select(ScenarioRisk).where(
                (ScenarioRisk.scenario_id == scenario_risk_from_repo.scenario_id)
                & (ScenarioRisk.risk_id == scenario_risk_from_repo.risk_id)
            )
        )
        assert scenario_risk_from_db is None

    def test_create_scenario_risk_assoc_through_repo_with_invalid_input(self, new_risk):
        # Arrange: Create non-existed scenario ID
        invalid_scenario_id = 10482

        # Act: Create Association with invalid scenario id should raise TypeError
        with pytest.raises(TypeError):
            self._create_assoc(
                risk_id=new_risk.id,
                scenario_id=invalid_scenario_id,
            )

    def test_create_scenario_risk_assoc_through_repo_with_non_existed_scenario(
        self, new_risk
    ):
        # Arrange: Create non-existed scenario ID
        non_existed_scenario_id = generate(size=13)

        # Act: Create Association with non existed scenario should raise ValueError
        with pytest.raises(ValueError):
            self._create_assoc(
                risk_id=new_risk.id,
                scenario_id=non_existed_scenario_id,
            )

    def test_create_scenario_risk_assoc_through_repo_with_non_existed_risk(
        self, new_scenario
    ):
        # Arrange: Create non-existed risk ID
        non_existed_risk_id = generate(size=13)

        # Act: Create Association with non existed scenario should raise ValueError
        with pytest.raises(ValueError):
            self._create_assoc(
                risk_id=non_existed_risk_id,
                scenario_id=new_scenario.id,
            )

    def test_get_non_existed_scenario_risk_assoc_by_id_through_repo(
        self, new_scenario, new_risk
    ):
        # Act: Get the assoc by compose id (but not create association yet)
        scenario_risk_get_by_id = ScenarioRiskRepo.get_by_id(
            scenario_id=new_scenario.id,
            risk_id=new_risk.id,
        )

        # Assert: The ScenarioRiskRepo should return None
        assert scenario_risk_get_by_id is None

    def test_update_scenario_risk_assoc_through_repo_while_changing_scenario(
        self, new_scenario, new_risk, default_account
    ):
        # Arrange: Get scenario and risk id
        scenario_id = new_scenario.id
        risk_id = new_risk.id

        # Arrange: Create Association
        assoc = self._create_assoc(risk_id=risk_id, scenario_id=scenario_id)

        # Arrange: Create another scenario
        another_scenario = create_scenario(default_account)
        another_scenario_id = another_scenario.id

        # Act: Change the assoc to another scenario id
        assoc.scenario_id = another_scenario_id

        # Assert: Save the updated object should raise ValueError as this assoc is not existed in another scenario
        with pytest.raises(ValueError):
            ScenarioRiskRepo.save(assoc)

    def test_delete_non_existed_scenario_risk_assoc_through_repo(
        self, new_scenario, new_risk
    ):
        # Arrange: Get scenario and risk id
        scenario_id = new_scenario.id
        risk_id = new_risk.id
        # Act: Delete the non existed assoc
        ScenarioRiskRepo.delete_by_id(
            scenario_id=scenario_id,
            risk_id=risk_id,
        )

        # Assert: Ensure the risk record is deleted from the database
        scenario_risk_from_db = db.session.scalar(
            sa.select(ScenarioRisk).where(
                (ScenarioRisk.scenario_id == scenario_id)
                & (ScenarioRisk.risk_id == risk_id)
            )
        )
        assert scenario_risk_from_db is None
