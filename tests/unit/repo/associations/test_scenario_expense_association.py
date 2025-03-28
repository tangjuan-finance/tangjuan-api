# from app.repository.associations import ScenarioExpenseRepo
# from app.infrastructure.models.associations import ScenarioExpense
# from tests.unit.factories import ExpenseDomainFactory, ScenarioDomainFactory
# import sqlalchemy as sa
# from app import db
# from decimal import Decimal


# class TestExpenseRepoCase:
#     def test_create_expense_domain_through_repo(self, default_account):
#         # Arrange: Create an expense and a scenario domain using the factory
#         default_max_yearly_growth_rate = Decimal("0.2")
#         scenario = ScenarioDomainFactory(owner=default_account)
#         expense = ExpenseDomainFactory(
#             owner=default_account, max_yearly_growth_rate=default_max_yearly_growth_rate
#         )

#         # Act: Save the expense domain to the scenario domain by ScenarioExpenseRepo, and get the association obj back from database
#         assoc_max_yearly_growth_rate = Decimal("0.7")
#         scenario_expense_from_repo = ScenarioExpenseRepo(
#             expense=expense,
#             scenario=scenario,
#             max_yearly_growth_rate=assoc_max_yearly_growth_rate,
#         )

#         scenario_expense_from_db = db.session.scalar(
#             sa.select(ScenarioExpense).where(
#                 (ScenarioExpense.scenario_id == scenario_expense_from_repo.scenario.id)
#                 and (
#                     ScenarioExpense.expense_id == scenario_expense_from_repo.expense.id
#                 )
#             )
#         )

#         # Assert: Ensure the values match between the domain object and the saved record
#         assert (
#             scenario_expense_from_repo.expense.id == scenario_expense_from_db.expense_id
#         )
#         assert (
#             scenario_expense_from_repo.scenario.id
#             == scenario_expense_from_db.scenario_id
#         )
#         assert (
#             scenario_expense_from_repo.max_yearly_growth_rate
#             == scenario_expense_from_db.max_yearly_growth_rate
#         )
#         assert (
#             scenario_expense_from_repo.max_yearly_growth_rate
#             == assoc_max_yearly_growth_rate
#         )
#         assert (
#             scenario_expense_from_repo.expense.max_yearly_growth_rate
#             == default_max_yearly_growth_rate
#         )
#         assert (
#             scenario_expense_from_repo.max_yearly_growth_rate
#             != scenario_expense_from_repo.expense.max_yearly_growth_rate
#         )

#     def test_update_expense_domain_through_repo(self, default_account):
#         # Arrange: Adding a expense to scenario using the ScenarioExpenseRepo
#         scenario = ScenarioDomainFactory(owner=default_account)
#         expense = ExpenseDomainFactory(owner=default_account)
#         default_max_yearly_growth_rate = Decimal("0.7")
#         scenario_expense_from_repo = ScenarioExpenseRepo(
#             expense=expense,
#             scenario=scenario,
#             max_yearly_growth_rate=default_max_yearly_growth_rate,
#         )
#         updated_max_yearly_growth_rate = Decimal("0.3")

#         # Act: Update the expense domain object (before saving)
#         scenario_expense_from_repo.max_yearly_growth_rate = (
#             updated_max_yearly_growth_rate
#         )

#         # Save the updated object through the repository and get the result
#         updated_scenario_expense = ScenarioExpenseRepo.save(scenario_expense_from_repo)

#         # Query the database to verify the updated expense record
#         scenario_expense_from_db = db.session.scalar(
#             sa.select(ScenarioExpense).where(
#                 (ScenarioExpense.scenario_id == scenario_expense_from_repo.scenario.id)
#                 and (
#                     ScenarioExpense.expense_id == scenario_expense_from_repo.expense.id
#                 )
#             )
#         )

#         # Assert: Ensure the values match between the domain object and the saved record
#         assert (
#             updated_scenario_expense.expense.id == scenario_expense_from_db.expense_id
#         )
#         assert (
#             updated_scenario_expense.scenario.id == scenario_expense_from_db.scenario_id
#         )
#         assert (
#             updated_scenario_expense.max_yearly_growth_rate
#             == scenario_expense_from_db.max_yearly_growth_rate
#         )
#         assert (
#             updated_scenario_expense.created_at == scenario_expense_from_db.created_at
#         )
#         assert (
#             updated_scenario_expense.updated_at == scenario_expense_from_db.updated_at
#         )
#         # Update_at from updated_expense should be different from the previous expense domain (the one before update)
#         assert (
#             updated_scenario_expense.updated_at != scenario_expense_from_repo.updated_at
#         )

#     def test_get_expense_domain_by_id_through_repo(self, default_account):
#         # Arrange: Create an expense domain using the factory
#         expense = ExpenseDomainFactory(owner=default_account)
#         expense_from_repo = ExpenseRepo.create(expense)

#         # Act: Update the expense domain object (before saving)
#         expense_get_by_id = ExpenseRepo.get_by_id(expense_from_repo.id)

#         # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
#         assert expense_get_by_id.id == expense_from_repo.id
#         assert expense_get_by_id.name == expense_from_repo.name

#     def test_get_expense_domain_list_through_repo(self, default_account):
#         # Arrange: Create an expense domain using the factory
#         origin_expense_list_length = len(ExpenseRepo.get_list())

#         # Act: Create 5 new expense domains
#         for _ in range(5):
#             expense = ExpenseDomainFactory(owner=default_account)
#             ExpenseRepo.create(expense)

#         # Assert: Ensure the list length is increased by 5
#         updated_expense_list_length = len(ExpenseRepo.get_list())
#         assert updated_expense_list_length == (origin_expense_list_length + 5)

#     def test_delete_expense_domain_through_repo(self, default_account):
#         # Arrange: Create an expense domain using the factory
#         expense = ExpenseDomainFactory(owner=default_account)
#         expense_from_repo = ExpenseRepo.create(expense)

#         # Act: Delete the expense domain object
#         ExpenseRepo.delete_by_id(expense_from_repo.id)

#         # Assert: Ensure the expense record is deleted from the database
#         assert (
#             db.session.scalar(
#                 sa.select(Expense).where(Expense.id == expense_from_repo.id)
#             )
#             is None
#         )
