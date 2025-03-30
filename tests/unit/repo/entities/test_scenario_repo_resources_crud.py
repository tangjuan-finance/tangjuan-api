from app.repository.entities import ScenarioRepo
from decimal import Decimal
from app.infrastructure.models import ScenarioExpense
from app.domain.entities import ExpenseDomain
from app import db
import sqlalchemy as sa
from tests.unit.repo.factories import create_expense


class TestScenarioRepoResourcesCrudCase:
    @staticmethod
    def _add_expense_to_scenario(expense, scenario):
        max_yearly_growth_rate = Decimal("1.2")
        attrs = {
            "max_yearly_growth_rate": max_yearly_growth_rate,
        }
        # Act: Add Expense to Scenario by ScenarioRepo
        return ScenarioRepo.add_resource(scenario=scenario, resrouce=expense, **attrs)

    # @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_add_resource_to_scenario_by_repo(new_expense, new_scenario):
        # Arrange: Creating Scenario and Resources
        max_yearly_growth_rate = Decimal("0.7")
        attrs = {
            "max_yearly_growth_rate": max_yearly_growth_rate,
        }
        # Act: Add Expense to Scenario by ScenarioRepo
        assoc_from_repo = ScenarioRepo.add_resource(
            scenario=new_scenario, resrouce=new_expense, **attrs
        )

        # Assert: Ensure the assoc are config as given
        assert assoc_from_repo.expense == new_expense
        assert assoc_from_repo.scenario == new_scenario
        assert assoc_from_repo.max_yearly_growth_rate == max_yearly_growth_rate

        # Assert: Ensure the assoc are stored in database
        assoc_from_db = db.session.scalars(
            sa.select(ScenarioExpense).where(
                (ScenarioExpense.scenario_id == new_scenario.id)
                & (ScenarioExpense.expense_id == new_expense.id)
            )
        ).first()

        assert assoc_from_db is not None  # Ensure record exists
        assert assoc_from_repo.expense.id == assoc_from_db.expense_id
        assert assoc_from_repo.scenario.id == assoc_from_db.scenario_id
        assert (
            assoc_from_repo.max_yearly_growth_rate
            == assoc_from_db.max_yearly_growth_rate
        )

    # @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_retrieve_resource_by_id_from_scenario_repo(
        self, new_expense, new_scenario
    ):
        # Arrange: Adding resource to scenario by id
        assoc_from_repo = self._add_expense_to_scenario(new_expense, new_scenario)

        # Act: Get resource from scenario repo by id
        assoc_get_by_id = ScenarioRepo.get_resource_by_id(
            scenario=new_scenario,
            resource_type=ExpenseDomain,
            resource_id=new_expense.id,
        )

        # Assert: Assert the assoc from get_resource_by_id is the same as assoc_from_repo
        assert assoc_get_by_id.expense.id == assoc_from_repo.expense.id
        assert assoc_get_by_id.scenario.id == assoc_from_repo.scenario.id

    # @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_retrieve_resource_list_from_scenario_repo(
        self, new_scenario, default_account
    ):
        # Arrange: Get the origin length of the collection
        origin_len = len(
            ScenarioRepo.get_resource_list(
                scenario=new_scenario, resource_type=ExpenseDomain
            )
        )

        # Arrange: Create 5 new assoc
        exp_list = [create_expense(default_account) for _ in range(5)]
        for exp in exp_list:
            self._add_expense_to_scenario(exp, new_scenario)

        # Act: Get resource list
        assoc_list = ScenarioRepo.get_resource_list(
            scenario=new_scenario, resource_type=ExpenseDomain
        )

        # Assert: Assert the assoc list
        for assoc in assoc_list:
            assert assoc.scenario.id == new_scenario.id
            assert assoc.expense in exp_list

        # Assert: Assert the assoc list and its length
        updated_len = len(assoc_list)
        assert updated_len == origin_len + 5

    # @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_update_resource_to_scenario_repo(self, new_expense, new_scenario):
        # Arrange: Create an Scenario Resource Assoc with default attr
        default_max_yearly_growth_rate = Decimal("0.7")
        attrs = {
            "max_yearly_growth_rate": default_max_yearly_growth_rate,
        }
        ScenarioRepo.add_resource(scenario=new_scenario, resrouce=new_expense, **attrs)

        # Act: Update the max_yearly_growth_rate
        updated_max_yearly_growth_rate = Decimal("0.3")
        updated_attrs = {
            "max_yearly_growth_rate": updated_max_yearly_growth_rate,
        }
        updated_assoc = ScenarioRepo.update_resource(
            scenario=new_scenario, resrouce=new_expense, **updated_attrs
        )

        # Assert: Ensure the update is successfully by checking the update_assoc attrs
        assert updated_assoc.max_yearly_growth_rate == updated_max_yearly_growth_rate

        # Assert: Ensure the update is successfully updated in database
        assoc_from_db = db.session.scalars(
            sa.select(ScenarioExpense).where(
                (ScenarioExpense.scenario_id == new_scenario.id)
                & (ScenarioExpense.expense_id == new_expense.id)
            )
        ).first()

        assert assoc_from_db is not None  # Ensure record exists
        assert (
            updated_assoc.max_yearly_growth_rate == assoc_from_db.max_yearly_growth_rate
        )

    # @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_delete_resource_from_scenario_repo(self, new_expense, new_scenario):
        # Arrange: Adding resource to scenario by id
        self._add_expense_to_scenario(new_expense, new_scenario)

        # Act: Delete the assoc from the scenario by repo
        ScenarioRepo.delete_resource(
            scenario=new_scenario,
            resource_type=ExpenseDomain,
            resource_id=new_expense.id,
        )

        # Assert: Check if assoc is deleted from repo
        assoc_from_repo = ScenarioRepo.get_resource_by_id(
            scenario=new_scenario,
            resource_type=ExpenseDomain,
            resource_id=new_expense.id,
        )
        assert assoc_from_repo is None

        # Assert: Check if assoc is deleted from database
        assoc_from_db = db.session.scalars(
            sa.select(ScenarioExpense).where(
                (ScenarioExpense.scenario_id == new_scenario.id)
                & (ScenarioExpense.expense_id == new_expense.id)
            )
        ).first()
        assert assoc_from_db is None
