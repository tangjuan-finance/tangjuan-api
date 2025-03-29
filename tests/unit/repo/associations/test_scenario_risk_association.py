from app.repository.associations import ScenarioRiskRepo
from app.infrastructure.models.associations import ScenarioRisk
from app.domain.associations import ScenarioRiskDomain
import sqlalchemy as sa
from app import db

from tests.unit.repo.factories import create_scenario, create_risk


class TestRiskRepoCase:
    @staticmethod
    def _create_assoc(risk, scenario):
        assoc_domain = ScenarioRiskDomain(
            risk=risk,
            scenario=scenario,
        )
        return ScenarioRiskRepo.create(assoc_domain)

    def test_create_scenario_risk_assoc_through_repo(self, new_scenario, new_risk):
        # Arrange: Create an risk and a scenario domain using the factory
        default_max_loss = 100000
        new_risk.max_loss = default_max_loss
        assoc_max_loss = 500000
        assoc_domain = ScenarioRiskDomain(
            risk=new_risk,
            scenario=new_scenario,
            max_loss=assoc_max_loss,
        )

        # Act: Save the risk domain to the scenario domain by ScenarioRiskRepo, and get the association obj back from database
        scenario_risk_from_repo = ScenarioRiskRepo.create(assoc_domain)

        scenario_risk_from_db = db.session.scalars(
            sa.select(ScenarioRisk).where(
                (ScenarioRisk.scenario_id == scenario_risk_from_repo.scenario.id)
                & (ScenarioRisk.risk_id == scenario_risk_from_repo.risk.id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_risk_from_repo.risk.id == scenario_risk_from_db.risk_id
        assert scenario_risk_from_repo.scenario.id == scenario_risk_from_db.scenario_id
        assert scenario_risk_from_repo.max_loss == scenario_risk_from_db.max_loss
        assert scenario_risk_from_repo.max_loss == assoc_max_loss
        assert scenario_risk_from_repo.risk.max_loss == default_max_loss
        assert scenario_risk_from_repo.max_loss != scenario_risk_from_repo.risk.max_loss

    def test_update_scenario_risk_assoc_through_repo(self, new_scenario, new_risk):
        # Arrange: Adding a risk to scenario using the ScenarioRiskRepo
        default_max_loss = 500000
        assoc_domain = ScenarioRiskDomain(
            risk=new_risk,
            scenario=new_scenario,
            max_loss=default_max_loss,
        )
        scenario_risk_from_repo = ScenarioRiskRepo.create(assoc_domain)
        updated_max_loss = 200000

        # Act: Update the risk domain object (before saving)
        scenario_risk_from_repo.max_loss = updated_max_loss

        # Save the updated object through the repository and get the result
        updated_scenario_risk = ScenarioRiskRepo.save(scenario_risk_from_repo)

        # Query the database to verify the updated risk record
        scenario_risk_from_db = db.session.scalars(
            sa.select(ScenarioRisk).where(
                (ScenarioRisk.scenario_id == scenario_risk_from_repo.scenario.id)
                & (ScenarioRisk.risk_id == scenario_risk_from_repo.risk.id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_scenario_risk.risk.id == scenario_risk_from_db.risk_id
        assert updated_scenario_risk.scenario.id == scenario_risk_from_db.scenario_id
        assert updated_scenario_risk.max_loss == updated_max_loss
        assert updated_scenario_risk.max_loss == scenario_risk_from_db.max_loss
        assert updated_scenario_risk.created_at == scenario_risk_from_db.created_at
        assert updated_scenario_risk.updated_at == scenario_risk_from_db.updated_at
        # Update_at from updated_risk should be different from the previous risk domain (the one before update)
        assert updated_scenario_risk.updated_at > scenario_risk_from_repo.updated_at

    def test_get_scenario_risk_assoc_by_id_through_repo(self, new_scenario, new_risk):
        # Arrange: Create an risk domain using the factory
        scenario_risk_from_repo = self._create_assoc(
            risk=new_risk, scenario=new_scenario
        )

        # Act: Update the risk domain object (before saving)
        scenario_risk_get_by_id = ScenarioRiskRepo.get_by_id(
            scenario_id=scenario_risk_from_repo.scenario.id,
            risk_id=scenario_risk_from_repo.risk.id,
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert (
            scenario_risk_get_by_id.scenario.id == scenario_risk_from_repo.scenario.id
        )
        assert scenario_risk_get_by_id.risk.id == scenario_risk_from_repo.risk.id

    def test_get_scenario_risk_assoc_list_through_repo(self, default_account):
        # Arrange: Create an risk domain using the factory
        origin_repo_list_length = len(ScenarioRiskRepo.get_list())

        # Act: Create 5 new risk domains
        for _ in range(5):
            new_scenario = create_scenario(default_account)
            new_risk = create_risk(default_account)
            self._create_assoc(risk=new_risk, scenario=new_scenario)

        # Assert: Ensure the list length is increased by 5
        updated_list_length = len(ScenarioRiskRepo.get_list())
        assert updated_list_length == (origin_repo_list_length + 5)

    def test_delete_scenario_risk_assoc_through_repo(self, new_scenario, new_risk):
        # Arrange: Create an risk domain using the factory
        scenario_risk_from_repo = self._create_assoc(
            risk=new_risk, scenario=new_scenario
        )

        # Act: Delete the risk domain object
        ScenarioRiskRepo.delete_by_id(
            scenario_id=scenario_risk_from_repo.scenario.id,
            risk_id=scenario_risk_from_repo.risk.id,
        )

        # Assert: Ensure the risk record is deleted from the database
        scenario_risk_from_db = db.session.scalar(
            sa.select(ScenarioRisk).where(
                (ScenarioRisk.scenario_id == scenario_risk_from_repo.scenario.id)
                & (ScenarioRisk.risk_id == scenario_risk_from_repo.risk.id)
            )
        )
        assert scenario_risk_from_db is None
