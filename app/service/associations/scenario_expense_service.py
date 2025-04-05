from app.domain.associations import ScenarioExpenseDomain
from app.repository.associations import ScenarioExpenseRepo
from app.repository.entities import ExpenseRepo
from .base import BaseAssociationService


class ScenarioExpenseService(BaseAssociationService):
    @classmethod
    def create_scenario_expense(cls, account_id: str, payload: dict) -> dict:
        """Create a new scenario expense assoc with validated owner."""

        scenario_id, expense_id = payload["scenario_id"], payload["expense_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_expense_ownership(account_id=account_id, expense_id=expense_id)

        # Create assoc based on payload
        assoc_domain = ScenarioExpenseDomain(**payload)
        assoc = ScenarioExpenseRepo.create(assoc_domain)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc)

    @classmethod
    def get_scenario_expense_by_id(cls, account_id: str, payload: dict) -> dict:
        """Get the scenario expense assoc by id with validated owner."""

        scenario_id, expense_id = payload["scenario_id"], payload["expense_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        cls._check_expense_ownership(account_id=account_id, expense_id=expense_id)

        # Get assoc by id
        assoc_from_repo = ScenarioExpenseRepo.get_by_id(
            scenario_id=scenario_id, expense_id=expense_id
        )

        if not assoc_from_repo:
            raise ValueError(
                f"Scenario Expense Association with scenario ID {scenario_id} and expense ID {expense_id} not found"
            )

        # Generate the response dict with the assoc
        return cls._create_response(assoc=assoc_from_repo)

    @classmethod
    def get_scenario_expenses(cls, account_id: str, payload: dict) -> list[dict]:
        """Get all scenario expense assoc with validated owner."""

        scenario_id = payload["scenario_id"]

        # Check if the account own both resources
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)

        # Generate the list of dict based on the assocs got from the repo
        return [
            cls._create_response(assoc=assoc)
            for assoc in ScenarioExpenseRepo.get_list(scenario_id=scenario_id)
        ]

    @classmethod
    def update_scenario_expense(cls, account_id: str, payload: dict) -> dict:
        """Update the scenario expense assoc with validated owner."""

        # Get the Scenario Expense Association
        assoc = cls.get_scenario_expense_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Update the Scenario Expense Association based on given payload
        for field in payload.keys():
            setattr(assoc, field, payload[field])

        # Set the change by repo
        updated_assoc = ScenarioExpenseRepo.save(assoc)

        # Generate the response dict with the assoc
        return cls._create_response(assoc=updated_assoc)

    @classmethod
    def delete_scenario_expense_by_id(cls, account_id: str, payload: dict) -> str:
        """Delete the scenario expense assoc by ID with validated owner."""
        # Get the Scenario Expense Association
        # Raises if not found or unauthorized
        cls.get_scenario_expense_by_id(account_id=account_id, payload=payload)[
            "association"
        ]

        # Get the scenario and expense ID
        scenario_id, expense_id = payload["scenario_id"], payload["expense_id"]

        # Delete the assoc
        ScenarioExpenseRepo.delete_by_id(scenario_id=scenario_id, expense_id=expense_id)

        return f"Scenario Expense with scenario ID {scenario_id} and expense ID {expense_id} deleted successfully"

    @staticmethod
    def _create_response(assoc: ScenarioExpenseDomain) -> dict:
        return {
            "association": assoc,
            "expense": ExpenseRepo.get_by_id(expense_id=assoc.expense_id),
        }

    @classmethod
    def _check_expense_ownership(cls, account_id: str, expense_id: str) -> str:
        if not isinstance(expense_id, str):
            raise TypeError(
                f"Expense ID should be type str, not type {type(expense_id).__name__}"
            )

        expense_from_repo = ExpenseRepo.get_by_id(expense_id=expense_id)

        if not expense_from_repo:
            raise ValueError(f"Expense with ID {expense_id} not found")

        cls._check_ownership_by_id(
            account_id=account_id, owner_id=expense_from_repo.owner.id
        )

        return "This account owned this expense"
