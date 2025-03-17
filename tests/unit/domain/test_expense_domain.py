# from app.domain.entities import ExpenseDomain


class TestExpenseDomainCase:
    def test_create_expense_domain(default_expense_domain, default_account_domain):
        # Assert
        assert default_expense_domain.name == "Default Expense Domain"
        assert default_expense_domain.amount == 50000
        assert default_expense_domain.max_yearly_growth_rate == 0.5
        assert default_expense_domain.min_yearly_growth_rate == -0.5
        assert default_expense_domain.start_age == 20
        assert default_expense_domain.owner_id == default_account_domain.id
