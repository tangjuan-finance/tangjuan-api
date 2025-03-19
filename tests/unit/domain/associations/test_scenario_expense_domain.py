# from app.domain.associations import ScenarioExpenseDomain
# from tests.unit.factories import ExpenseDomainFactory


# class TestScenarioExpenseDomainCase:
#     def test_create_scenario_expense_domain(
#         default_expense_domain, default_account_domain
#     ):
#         # Assign
#         expense1 = ExpenseDomainFactory(
#             name="expense1",
#         )
#         expense2 = ExpenseDomainFactory(
#             name="expense2",
#         )
#         # Act
#         scenario_expense = ScenarioExpenseDomain()
#         # Assert
#         assert default_expense_domain.name == "Default Expense Domain"
#         assert default_expense_domain.amount == 50000
#         assert default_expense_domain.max_yearly_growth_rate == 0.5
#         assert default_expense_domain.min_yearly_growth_rate == -0.5
#         assert default_expense_domain.start_age == 20
#         assert default_expense_domain.owner_id == default_account_domain.id
