from app.repository.associations import ScenarioIncomeRepo
from app.infrastructure.models.associations import ScenarioIncome
from app.domain.associations import ScenarioIncomeDomain
import sqlalchemy as sa
from app import db
from decimal import Decimal

from tests.unit.repo.factories import create_income, create_scenario
from nanoid import generate
import pytest


class TestIncomeRepoCase:
    @staticmethod
    def _create_assoc(income_id, scenario_id):
        assoc_domain = ScenarioIncomeDomain(
            income_id=income_id,
            scenario_id=scenario_id,
        )
        return ScenarioIncomeRepo.create(assoc_domain)

    def test_create_scenario_income_assoc_through_repo(self, new_scenario, new_income):
        # Arrange: Create an income and a scenario domain using the factory
        default_max_yearly_growth_rate = Decimal("0.2")
        new_income.max_yearly_growth_rate = default_max_yearly_growth_rate
        assoc_max_yearly_growth_rate = Decimal("0.7")

        # Create Assoc Domain
        assoc_domain = ScenarioIncomeDomain(
            income_id=new_income.id,
            scenario_id=new_scenario.id,
            max_yearly_growth_rate=assoc_max_yearly_growth_rate,
        )

        # Act: Save the income domain to the scenario domain by ScenarioIncomeRepo, and get the association obj back from database
        scenario_income_from_repo = ScenarioIncomeRepo.create(assoc_domain)

        scenario_income_from_db = db.session.scalars(
            sa.select(ScenarioIncome).where(
                (ScenarioIncome.scenario_id == scenario_income_from_repo.scenario_id)
                & (ScenarioIncome.income_id == scenario_income_from_repo.income_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_income_from_repo.income_id == scenario_income_from_db.income_id
        assert (
            scenario_income_from_repo.scenario_id == scenario_income_from_db.scenario_id
        )
        assert (
            scenario_income_from_repo.max_yearly_growth_rate
            == scenario_income_from_db.max_yearly_growth_rate
        )
        assert (
            scenario_income_from_repo.max_yearly_growth_rate
            == assoc_max_yearly_growth_rate
        )

    def test_update_scenario_income_assoc_through_repo(self, new_scenario, new_income):
        # Arrange: Adding a income to scenario using the ScenarioIncomeRepo
        default_max_yearly_growth_rate = Decimal("0.7")
        assoc_domain = ScenarioIncomeDomain(
            income_id=new_income.id,
            scenario_id=new_scenario.id,
            max_yearly_growth_rate=default_max_yearly_growth_rate,
        )
        scenario_income_from_repo = ScenarioIncomeRepo.create(assoc_domain)
        updated_max_yearly_growth_rate = Decimal("0.2")

        # Act: Update the income domain object (before saving)
        scenario_income_from_repo.max_yearly_growth_rate = (
            updated_max_yearly_growth_rate
        )

        # Save the updated object through the repository and get the result
        updated_scenario_income = ScenarioIncomeRepo.save(scenario_income_from_repo)

        # Query the database to verify the updated income record
        scenario_income_from_db = db.session.scalars(
            sa.select(ScenarioIncome).where(
                (ScenarioIncome.scenario_id == scenario_income_from_repo.scenario_id)
                & (ScenarioIncome.income_id == scenario_income_from_repo.income_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_scenario_income.income_id == scenario_income_from_db.income_id
        assert (
            updated_scenario_income.scenario_id == scenario_income_from_db.scenario_id
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

    def test_get_scenario_income_assoc_by_id_through_repo(
        self, new_scenario, new_income
    ):
        # Arrange: Create an income domain using the factory
        scenario_income_from_repo = self._create_assoc(
            income_id=new_income.id,
            scenario_id=new_scenario.id,
        )

        # Act: Update the income domain object (before saving)
        scenario_income_get_by_id = ScenarioIncomeRepo.get_by_id(
            scenario_id=scenario_income_from_repo.scenario_id,
            income_id=scenario_income_from_repo.income_id,
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert (
            scenario_income_get_by_id.scenario_id
            == scenario_income_from_repo.scenario_id
        )
        assert (
            scenario_income_get_by_id.income_id == scenario_income_from_repo.income_id
        )

    def test_get_scenario_income_assoc_list_through_repo(
        self, default_account, new_scenario
    ):
        # Arrange: Create an income domain using the factory
        origin_repo_list_length = len(
            ScenarioIncomeRepo.get_list(scenario_id=new_scenario.id)
        )

        # Act: Create 5 new income domains
        for _ in range(5):
            new_income = create_income(default_account)
            self._create_assoc(
                income_id=new_income.id,
                scenario_id=new_scenario.id,
            )

        # Assert: Ensure the list length is increased by 5
        updated_list_length = len(
            ScenarioIncomeRepo.get_list(scenario_id=new_scenario.id)
        )
        assert updated_list_length == (origin_repo_list_length + 5)

    def test_delete_scenario_income_assoc_through_repo(self, new_scenario, new_income):
        # Arrange: Create an income domain using the factory
        scenario_income_from_repo = self._create_assoc(
            income_id=new_income.id,
            scenario_id=new_scenario.id,
        )

        # Act: Delete the income domain object
        ScenarioIncomeRepo.delete_by_id(
            scenario_id=scenario_income_from_repo.scenario_id,
            income_id=scenario_income_from_repo.income_id,
        )

        # Assert: Ensure the income record is deleted from the database
        scenario_income_from_db = db.session.scalar(
            sa.select(ScenarioIncome).where(
                (ScenarioIncome.scenario_id == scenario_income_from_repo.scenario_id)
                & (ScenarioIncome.income_id == scenario_income_from_repo.income_id)
            )
        )
        assert scenario_income_from_db is None

    def test_create_scenario_income_assoc_through_repo_with_invalid_input(
        self, new_income
    ):
        # Arrange: Create non-existed scenario ID
        invalid_scenario_id = 10482

        # Act: Create Association with invalid scenario id should raise TypeError
        with pytest.raises(TypeError):
            self._create_assoc(
                income_id=new_income.id,
                scenario_id=invalid_scenario_id,
            )

    def test_create_scenario_income_assoc_through_repo_with_non_existed_scenario(
        self, new_income
    ):
        # Arrange: Create non-existed scenario ID
        non_existed_scenario_id = generate(size=13)

        # Act: Create Association with non existed scenario should raise ValueError
        with pytest.raises(ValueError):
            self._create_assoc(
                income_id=new_income.id,
                scenario_id=non_existed_scenario_id,
            )

    def test_create_scenario_income_assoc_through_repo_with_non_existed_income(
        self, new_scenario
    ):
        # Arrange: Create non-existed income ID
        non_existed_income_id = generate(size=13)

        # Act: Create Association with non existed scenario should raise ValueError
        with pytest.raises(ValueError):
            self._create_assoc(
                income_id=non_existed_income_id,
                scenario_id=new_scenario.id,
            )

    def test_get_non_existed_scenario_income_assoc_by_id_through_repo(
        self, new_scenario, new_income
    ):
        # Act: Get the assoc by compose id (but not create association yet)
        scenario_income_get_by_id = ScenarioIncomeRepo.get_by_id(
            scenario_id=new_scenario.id,
            income_id=new_income.id,
        )

        # Assert: The ScenarioIncomeRepo should return None
        assert scenario_income_get_by_id is None

    def test_update_scenario_income_assoc_through_repo_while_changing_scenario(
        self, new_scenario, new_income, default_account
    ):
        # Arrange: Get scenario and income id
        scenario_id = new_scenario.id
        income_id = new_income.id

        # Arrange: Create Association
        assoc = self._create_assoc(income_id=income_id, scenario_id=scenario_id)

        # Arrange: Create another scenario
        another_scenario = create_scenario(default_account)
        another_scenario_id = another_scenario.id

        # Act: Change the assoc to another scenario id
        assoc.scenario_id = another_scenario_id

        # Assert: Save the updated object should raise ValueError as this assoc is not existed in another scenario
        with pytest.raises(ValueError):
            ScenarioIncomeRepo.save(assoc)

    def test_delete_non_existed_scenario_income_assoc_through_repo(
        self, new_scenario, new_income
    ):
        # Arrange: Get scenario and income id
        scenario_id = new_scenario.id
        income_id = new_income.id
        # Act: Delete the non existed assoc
        ScenarioIncomeRepo.delete_by_id(
            scenario_id=scenario_id,
            income_id=income_id,
        )

        # Assert: Ensure the income record is deleted from the database
        scenario_income_from_db = db.session.scalar(
            sa.select(ScenarioIncome).where(
                (ScenarioIncome.scenario_id == scenario_id)
                & (ScenarioIncome.income_id == income_id)
            )
        )
        assert scenario_income_from_db is None
