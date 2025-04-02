from app.repository.associations import ScenarioExpenseRepo
from app.infrastructure.models.associations import ScenarioExpense
from app.domain.associations import ScenarioExpenseDomain
import sqlalchemy as sa
from app import db
from decimal import Decimal

from tests.unit.repo.factories import create_expense, create_scenario

# Revised start from here
from nanoid import generate
import pytest


class TestExpenseRepoCase:
    @staticmethod
    def _create_assoc(expense_id, scenario_id):
        assoc_domain = ScenarioExpenseDomain(
            expense_id=expense_id,
            scenario_id=scenario_id,
        )
        return ScenarioExpenseRepo.create(assoc_domain)

    def test_create_scenario_expense_assoc_through_repo(
        self, new_scenario, new_expense
    ):
        # Arrange: Create an expense and a scenario domain using the factory
        default_max_yearly_growth_rate = Decimal("0.2")
        new_expense.max_yearly_growth_rate = default_max_yearly_growth_rate
        assoc_max_yearly_growth_rate = Decimal("0.7")

        # Create Assoc Domain
        assoc_domain = ScenarioExpenseDomain(
            expense_id=new_expense.id,
            scenario_id=new_scenario.id,
            max_yearly_growth_rate=assoc_max_yearly_growth_rate,
        )

        # Act: Save the expense domain to the scenario domain by ScenarioExpenseRepo, and get the association obj back from database
        scenario_expense_from_repo = ScenarioExpenseRepo.create(assoc_domain)

        scenario_expense_from_db = db.session.scalars(
            sa.select(ScenarioExpense).where(
                (ScenarioExpense.scenario_id == scenario_expense_from_repo.scenario_id)
                & (ScenarioExpense.expense_id == scenario_expense_from_repo.expense_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert (
            scenario_expense_from_repo.expense_id == scenario_expense_from_db.expense_id
        )
        assert (
            scenario_expense_from_repo.scenario_id
            == scenario_expense_from_db.scenario_id
        )
        assert (
            scenario_expense_from_repo.max_yearly_growth_rate
            == scenario_expense_from_db.max_yearly_growth_rate
        )
        assert (
            scenario_expense_from_repo.max_yearly_growth_rate
            == assoc_max_yearly_growth_rate
        )

    def test_update_scenario_expense_assoc_through_repo(
        self, new_scenario, new_expense
    ):
        # Arrange: Adding a expense to scenario using the ScenarioExpenseRepo
        default_max_yearly_growth_rate = Decimal("0.7")
        assoc_domain = ScenarioExpenseDomain(
            expense_id=new_expense.id,
            scenario_id=new_scenario.id,
            max_yearly_growth_rate=default_max_yearly_growth_rate,
        )
        scenario_expense_from_repo = ScenarioExpenseRepo.create(assoc_domain)
        updated_max_yearly_growth_rate = Decimal("0.2")

        # Act: Update the expense domain object (before saving)
        scenario_expense_from_repo.max_yearly_growth_rate = (
            updated_max_yearly_growth_rate
        )

        # Save the updated object through the repository and get the result
        updated_scenario_expense = ScenarioExpenseRepo.save(scenario_expense_from_repo)

        # Query the database to verify the updated expense record
        scenario_expense_from_db = db.session.scalars(
            sa.select(ScenarioExpense).where(
                (ScenarioExpense.scenario_id == scenario_expense_from_repo.scenario_id)
                & (ScenarioExpense.expense_id == scenario_expense_from_repo.expense_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert (
            updated_scenario_expense.expense_id == scenario_expense_from_db.expense_id
        )
        assert (
            updated_scenario_expense.scenario_id == scenario_expense_from_db.scenario_id
        )
        assert (
            updated_scenario_expense.max_yearly_growth_rate
            == updated_max_yearly_growth_rate
        )
        assert (
            updated_scenario_expense.max_yearly_growth_rate
            == scenario_expense_from_db.max_yearly_growth_rate
        )
        assert (
            updated_scenario_expense.created_at == scenario_expense_from_db.created_at
        )
        assert (
            updated_scenario_expense.updated_at == scenario_expense_from_db.updated_at
        )
        # Update_at from updated_expense should be different from the previous expense domain (the one before update)
        assert (
            updated_scenario_expense.updated_at > scenario_expense_from_repo.updated_at
        )

    def test_get_scenario_expense_assoc_by_id_through_repo(
        self, new_scenario, new_expense
    ):
        # Arrange: Create an expense domain using the factory
        scenario_expense_from_repo = self._create_assoc(
            expense_id=new_expense.id,
            scenario_id=new_scenario.id,
        )

        # Act: Update the expense domain object (before saving)
        scenario_expense_get_by_id = ScenarioExpenseRepo.get_by_id(
            scenario_id=scenario_expense_from_repo.scenario_id,
            expense_id=scenario_expense_from_repo.expense_id,
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert (
            scenario_expense_get_by_id.scenario_id
            == scenario_expense_from_repo.scenario_id
        )
        assert (
            scenario_expense_get_by_id.expense_id
            == scenario_expense_from_repo.expense_id
        )

    def test_get_scenario_expense_assoc_list_through_repo(
        self, default_account, new_scenario
    ):
        # Arrange: Create an expense domain using the factory
        origin_repo_list_length = len(
            ScenarioExpenseRepo.get_list(scenario_id=new_scenario.id)
        )

        # Act: Create 5 new expense domains
        for _ in range(5):
            new_expense = create_expense(default_account)
            self._create_assoc(
                expense_id=new_expense.id,
                scenario_id=new_scenario.id,
            )

        # Assert: Ensure the list length is increased by 5
        updated_list_length = len(
            ScenarioExpenseRepo.get_list(scenario_id=new_scenario.id)
        )
        assert updated_list_length == (origin_repo_list_length + 5)

    def test_delete_scenario_expense_assoc_through_repo(
        self, new_scenario, new_expense
    ):
        # Arrange: Create an expense domain using the factory
        scenario_expense_from_repo = self._create_assoc(
            expense_id=new_expense.id,
            scenario_id=new_scenario.id,
        )

        # Act: Delete the expense domain object
        ScenarioExpenseRepo.delete_by_id(
            scenario_id=scenario_expense_from_repo.scenario_id,
            expense_id=scenario_expense_from_repo.expense_id,
        )

        # Assert: Ensure the expense record is deleted from the database
        scenario_expense_from_db = db.session.scalar(
            sa.select(ScenarioExpense).where(
                (ScenarioExpense.scenario_id == scenario_expense_from_repo.scenario_id)
                & (ScenarioExpense.expense_id == scenario_expense_from_repo.expense_id)
            )
        )
        assert scenario_expense_from_db is None

    # Revised start from here

    def test_create_scenario_expense_assoc_through_repo_with_invalid_input(
        self, new_expense
    ):
        # Arrange: Create non-existed scenario ID
        invalid_scenario_id = 10482

        # Act: Create Association with invalid scenario id should raise TypeError
        with pytest.raises(TypeError):
            self._create_assoc(
                expense_id=new_expense.id,
                scenario_id=invalid_scenario_id,
            )

    def test_create_scenario_expense_assoc_through_repo_with_non_existed_scenario(
        self, new_expense
    ):
        # Arrange: Create non-existed scenario ID
        non_existed_scenario_id = generate(size=13)

        # Act: Create Association with non existed scenario should raise ValueError
        with pytest.raises(ValueError):
            self._create_assoc(
                expense_id=new_expense.id,
                scenario_id=non_existed_scenario_id,
            )

    def test_create_scenario_expense_assoc_through_repo_with_non_existed_expense(
        self, new_scenario
    ):
        # Arrange: Create non-existed expense ID
        non_existed_expense_id = generate(size=13)

        # Act: Create Association with non existed scenario should raise ValueError
        with pytest.raises(ValueError):
            self._create_assoc(
                expense_id=non_existed_expense_id,
                scenario_id=new_scenario.id,
            )

    def test_get_non_existed_scenario_expense_assoc_by_id_through_repo(
        self, new_scenario, new_expense
    ):
        # Act: Get the assoc by compose id (but not create association yet)
        scenario_expense_get_by_id = ScenarioExpenseRepo.get_by_id(
            scenario_id=new_scenario.id,
            expense_id=new_expense.id,
        )

        # Assert: The ScenarioExpenseRepo should return None
        assert scenario_expense_get_by_id is None

    def test_update_scenario_expense_assoc_through_repo_while_changing_scenario(
        self, new_scenario, new_expense, default_account
    ):
        # Arrange: Get scenario and expense id
        scenario_id = new_scenario.id
        expense_id = new_expense.id

        # Arrange: Create Association
        assoc = self._create_assoc(expense_id=expense_id, scenario_id=scenario_id)

        # Arrange: Create another scenario
        another_scenario = create_scenario(default_account)
        another_scenario_id = another_scenario.id

        # Act: Change the assoc to another scenario id
        assoc.scenario_id = another_scenario_id

        # Assert: Save the updated object should raise ValueError as this assoc is not existed in another scenario
        with pytest.raises(ValueError):
            ScenarioExpenseRepo.save(assoc)

    def test_delete_non_existed_scenario_expense_assoc_through_repo(
        self, new_scenario, new_expense
    ):
        # Arrange: Get scenario and expense id
        scenario_id = new_scenario.id
        expense_id = new_expense.id
        # Act: Delete the non existed assoc
        ScenarioExpenseRepo.delete_by_id(
            scenario_id=scenario_id,
            expense_id=expense_id,
        )

        # Assert: Ensure the expense record is deleted from the database
        scenario_expense_from_db = db.session.scalar(
            sa.select(ScenarioExpense).where(
                (ScenarioExpense.scenario_id == scenario_id)
                & (ScenarioExpense.expense_id == expense_id)
            )
        )
        assert scenario_expense_from_db is None
