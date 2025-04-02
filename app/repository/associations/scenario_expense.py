from app.domain.associations import ScenarioExpenseDomain
from app.infrastructure.models import ScenarioExpense, Scenario, Expense
from app import db
import sqlalchemy as sa
from sqlalchemy.orm.exc import NoResultFound


class ScenarioExpenseRepo:
    @staticmethod
    def create(assoc: ScenarioExpenseDomain) -> ScenarioExpenseDomain:
        """Given an Associaiton Domain Object, store it in the database and return the stored object."""
        # Check if the association already exists
        scenario_id = assoc.scenario_id
        expense_id = assoc.expense_id
        existing_assoc = ScenarioExpenseRepo._get_assoc_model_by_cid(
            scenario_id=scenario_id, expense_id=expense_id
        )
        if existing_assoc:
            raise ValueError(
                f"Scenario Expense Record with scenario_id {assoc.scenario_id}, expense_id {assoc.expense_id} already exists!"
            )

        # Instance with required attr
        # Optional attr would be None, which is set in Domain Definition
        assoc_model = ScenarioExpense(
            scenario_id=scenario_id,
            expense_id=expense_id,
            max_yearly_growth_rate=assoc.max_yearly_growth_rate,
            min_yearly_growth_rate=assoc.min_yearly_growth_rate,
            start_age=assoc.start_age,
            end_age=assoc.end_age,
            memo=assoc.memo,
        )

        # Save the Expense model to the database
        db.session.add(assoc_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioExpenseRepo._map_to_domain(assoc_model)

    @staticmethod
    def save(assoc: ScenarioExpenseDomain) -> ScenarioExpenseDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get expense_model from database
        existing_assoc = ScenarioExpenseRepo._get_assoc_model_by_cid(
            assoc.scenario_id, assoc.expense_id
        )
        if not existing_assoc:
            raise ValueError(
                f"Scenario Expense Record with scenario_id {assoc.scenario_id}, expense_id {assoc.expense_id} not found"
            )
        # As existing_assoc is query by scenario_id and expense_id, both id of existing_assoc would be the same as assoc
        existing_assoc.max_yearly_growth_rate = assoc.max_yearly_growth_rate
        existing_assoc.min_yearly_growth_rate = assoc.min_yearly_growth_rate
        existing_assoc.start_age = assoc.start_age
        existing_assoc.end_age = assoc.end_age
        existing_assoc.memo = assoc.memo

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioExpenseRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_by_id(scenario_id: str, expense_id: str) -> ScenarioExpenseDomain | None:
        """Retrieve an expense by ID and return as DomainObject."""
        # Get expense_model from database
        existing_assoc = ScenarioExpenseRepo._get_assoc_model_by_cid(
            scenario_id, expense_id
        )

        if not existing_assoc:
            return None

        # Return the domain object with attributes populated from the database
        return ScenarioExpenseRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_list(scenario_id: str) -> list[ScenarioExpenseDomain]:
        """Retrieve all expenses and return as a list of DomainObjects."""
        assoc_model_list = db.session.scalars(
            sa.select(ScenarioExpense).where(
                (ScenarioExpense.scenario_id == scenario_id)
            )
        ).all()

        return [
            ScenarioExpenseRepo._map_to_domain(
                assoc,
            )
            for assoc in assoc_model_list
        ]

    @staticmethod
    def delete_by_id(scenario_id: str, expense_id: str) -> None:
        """Given an expense ID, remove it from the database."""
        # Get expense_model from database
        existing_assoc = ScenarioExpenseRepo._get_assoc_model_by_cid(
            scenario_id, expense_id
        )

        if existing_assoc:
            db.session.delete(existing_assoc)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(assoc_model: ScenarioExpense) -> ScenarioExpenseDomain:
        """Helper method to map the ScenarioExpense model to a ScenarioExpenseDomain object."""
        return ScenarioExpenseDomain(
            scenario_id=assoc_model.scenario_id,
            expense_id=assoc_model.expense_id,
            max_yearly_growth_rate=assoc_model.max_yearly_growth_rate,
            min_yearly_growth_rate=assoc_model.min_yearly_growth_rate,
            start_age=assoc_model.start_age,
            end_age=assoc_model.end_age,
            memo=assoc_model.memo,
            created_at=assoc_model.created_at,
            updated_at=assoc_model.updated_at,
        )

    @staticmethod
    def _get_assoc_model_by_cid(scenario_id: str, expense_id: str) -> ScenarioExpense:
        # Check if scenario existed
        ScenarioExpenseRepo._check_if_scenario_existed_by_id(scenario_id)

        # Check if expense existed
        ScenarioExpenseRepo._check_if_expense_existed_by_id(expense_id)

        # Get assoc by checked scenario and expense id
        assoc = db.session.scalar(
            sa.select(ScenarioExpense).where(
                (ScenarioExpense.scenario_id == scenario_id)
                & (ScenarioExpense.expense_id == expense_id)
            )
        )
        return assoc

    @staticmethod
    def _check_if_scenario_existed_by_id(scenario_id: str) -> str:
        if not isinstance(scenario_id, str):
            raise TypeError("scenario_id shoud be type str")
        try:
            db.session.get_one(Scenario, scenario_id)
        except NoResultFound:
            raise ValueError("Scenario not found!")

        return f"Scenario {scenario_id} existed."

    @staticmethod
    def _check_if_expense_existed_by_id(expense_id: str) -> str:
        if not isinstance(expense_id, str):
            raise TypeError("expense_id shoud be type str")
        try:
            db.session.get_one(Expense, expense_id)
        except NoResultFound:
            raise ValueError("Expense not found!")

        return f"Expense {expense_id} existed."
