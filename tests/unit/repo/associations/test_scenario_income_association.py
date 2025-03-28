from app.repository.associations import ScenarioIncomeRepo
from app.infrastructure.models.associations import ScenarioIncome
from app.domain.associations import ScenarioIncomeDomain
from tests.unit.factories import IncomeDomainFactory, ScenarioDomainFactory
import sqlalchemy as sa
from app import db
from decimal import Decimal


class TestIncomeRepoCase:
    def _create_assoc(self, default_account):
        scenario = ScenarioDomainFactory(owner=default_account)
        income = IncomeDomainFactory(owner=default_account)
        assoc_domain = ScenarioIncomeDomain(
            income=income,
            scenario=scenario,
        )
        return ScenarioIncomeRepo.create(assoc_domain)

    def test_create_scenario_income_assoc_through_repo(self, default_account):
        # Arrange: Create an income and a scenario domain using the factory
        default_max_yearly_growth_rate = Decimal("0.2")
        scenario = ScenarioDomainFactory(owner=default_account)
        income = IncomeDomainFactory(
            owner=default_account, max_yearly_growth_rate=default_max_yearly_growth_rate
        )
        assoc_max_yearly_growth_rate = Decimal("0.7")
        assoc_domain = ScenarioIncomeDomain(
            income=income,
            scenario=scenario,
            max_yearly_growth_rate=assoc_max_yearly_growth_rate,
        )

        # Act: Save the income domain to the scenario domain by ScenarioIncomeRepo, and get the association obj back from database
        scenario_income_from_repo = ScenarioIncomeRepo.create(assoc_domain)

        scenario_income_from_db = db.session.scalar(
            sa.select(ScenarioIncome).where(
                (ScenarioIncome.scenario_id == scenario_income_from_repo.scenario.id)
                & (ScenarioIncome.income_id == scenario_income_from_repo.income.id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_income_from_repo.income.id == scenario_income_from_db.income_id
        assert (
            scenario_income_from_repo.scenario.id == scenario_income_from_db.scenario_id
        )
        assert (
            scenario_income_from_repo.max_yearly_growth_rate
            == scenario_income_from_db.max_yearly_growth_rate
        )
        assert (
            scenario_income_from_repo.max_yearly_growth_rate
            == assoc_max_yearly_growth_rate
        )
        assert (
            scenario_income_from_repo.income.max_yearly_growth_rate
            == default_max_yearly_growth_rate
        )
        assert (
            scenario_income_from_repo.max_yearly_growth_rate
            != scenario_income_from_repo.income.max_yearly_growth_rate
        )

    def test_update_scenario_income_assoc_through_repo(self, default_account):
        # Arrange: Adding a income to scenario using the ScenarioIncomeRepo
        scenario = ScenarioDomainFactory(owner=default_account)
        income = IncomeDomainFactory(owner=default_account)
        default_max_yearly_growth_rate = Decimal("0.7")
        assoc_domain = ScenarioIncomeDomain(
            income=income,
            scenario=scenario,
            max_yearly_growth_rate=default_max_yearly_growth_rate,
        )
        scenario_income_from_repo = ScenarioIncomeRepo.create(assoc_domain)
        updated_max_yearly_growth_rate = Decimal("0.3")

        # Act: Update the income domain object (before saving)
        scenario_income_from_repo.max_yearly_growth_rate = (
            updated_max_yearly_growth_rate
        )

        # Save the updated object through the repository and get the result
        updated_scenario_income = ScenarioIncomeRepo.save(scenario_income_from_repo)

        # Query the database to verify the updated income record
        scenario_income_from_db = db.session.scalars(
            sa.select(ScenarioIncome).where(
                (ScenarioIncome.scenario_id == scenario_income_from_repo.scenario.id)
                & (ScenarioIncome.income_id == scenario_income_from_repo.income.id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_scenario_income.income.id == scenario_income_from_db.income_id
        assert (
            updated_scenario_income.scenario.id == scenario_income_from_db.scenario_id
        )
        assert (
            updated_scenario_income.max_yearly_growth_rate
            == updated_max_yearly_growth_rate
        )
        assert (
            updated_scenario_income.max_yearly_growth_rate
            == scenario_income_from_db.max_yearly_growth_rate
        )
        assert updated_scenario_income.created_at == scenario_income_from_db.created_at
        assert updated_scenario_income.updated_at == scenario_income_from_db.updated_at
        # Update_at from updated_income should be different from the previous income domain (the one before update)
        assert updated_scenario_income.updated_at > scenario_income_from_repo.updated_at

    def test_get_scenario_income_assoc_by_id_through_repo(self, default_account):
        # Arrange: Create an income domain using the factory
        scenario_income_from_repo = self._create_assoc(default_account)

        # Act: Update the income domain object (before saving)
        scenario_income_get_by_id = ScenarioIncomeRepo.get_by_id(
            scenario_id=scenario_income_from_repo.scenario.id,
            income_id=scenario_income_from_repo.income.id,
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert (
            scenario_income_get_by_id.scenario_id
            == scenario_income_from_repo.scenario_id
        )
        assert (
            scenario_income_get_by_id.income_id == scenario_income_from_repo.income_id
        )

    def test_get_scenario_income_assoc_list_through_repo(self, default_account):
        # Arrange: Create an income domain using the factory
        origin_repo_list_length = len(ScenarioIncomeRepo.get_list())

        # Act: Create 5 new income domains
        for _ in range(5):
            self._create_assoc(default_account)

        # Assert: Ensure the list length is increased by 5
        updated_list_length = len(ScenarioIncomeRepo.get_list())
        assert updated_list_length == (origin_repo_list_length + 5)

    def test_delete_scenario_income_assoc_through_repo(self, default_account):
        # Arrange: Create an income domain using the factory
        scenario_income_from_repo = self._create_assoc(default_account)

        # Act: Delete the income domain object
        ScenarioIncomeRepo.delete_by_id(scenario_income_from_repo.id)

        # Assert: Ensure the income record is deleted from the database
        scenario_income_from_db = db.session.scalars(
            sa.select(ScenarioIncomeRepo).where(
                (ScenarioIncome.scenario_id == scenario_income_from_repo.scenario.id)
                & (ScenarioIncome.income_id == scenario_income_from_repo.income.id)
            )
        )
        assert scenario_income_from_db is None
