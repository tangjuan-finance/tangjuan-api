import factory
from app.domain.entities import (
    AccountDomain,
    ChildDomain,
    AssetDomain,
    ExpenseDomain,
    HouseDomain,
    IncomeDomain,
    LiabilityDomain,
    RiskDomain,
    ScenarioDomain,
)


class AccountDomainFactory(factory.Factory):
    """Factory for AccountDomain"""

    class Meta:
        model = AccountDomain

    username = factory.Faker("user_name")
    email = factory.Faker("email")

    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        """Set default password"""
        password = extracted if extracted else factory.Faker("password", length=12)
        obj.set_password(password)


class ChildDomainFactory(factory.Factory):
    """Factory for ChildDomain"""

    class Meta:
        model = ChildDomain

    name = factory.Faker("text", max_nb_chars=20).rstrip(".")
    birth_age = factory.Faker("random_int", min=20, max=50)
    independent_age = factory.LazyAttribute(lambda o: o.birth_age + 20)
    owner = factory.SubFactory(AccountDomainFactory)


class AssetDomainFactory(factory.Factory):
    """Factory for AssetDomain"""

    class Meta:
        model = AssetDomain

    name = factory.Faker("text", max_nb_chars=20).rstrip(".")
    amount = factory.Faker("random_int", min=10000, max=1000000)
    max_yearly_return_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=0.06, max_value=1.0
    )
    min_yearly_return_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=-1.0, max_value=0.05
    )
    start_age = factory.Faker("random_int", min=20, max=65)
    owner = factory.SubFactory(AccountDomainFactory)


class ExpenseDomainFactory(factory.Factory):
    """Factory for ExpenseDomain"""

    class Meta:
        model = ExpenseDomain

    name = factory.Faker("text", max_nb_chars=20).rstrip(".")
    amount = factory.Faker("random_int", min=1000, max=100000)
    max_yearly_growth_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=0.01, max_value=0.5
    )
    min_yearly_growth_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=-0.5, max_value=0
    )
    start_age = factory.Faker("random_int", min=20, max=65)
    owner = factory.SubFactory(AccountDomainFactory)


class HouseDomainFactory(factory.Factory):
    """Factory for HouseDomain"""

    class Meta:
        model = HouseDomain

    name = factory.Faker("text", max_nb_chars=20).rstrip(".")
    amount = factory.Faker("random_int", min=100000, max=5000000)
    down_payment = factory.Faker("random_int", min=10000, max=500000)
    interest_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=1.0, max_value=5.0
    )
    loan_term = factory.Faker("random_int", min=10, max=40)
    purchase_age = factory.Faker("random_int", min=20, max=65)
    owner = factory.SubFactory(AccountDomainFactory)


class IncomeDomainFactory(factory.Factory):
    """Factory for IncomeDomain"""

    class Meta:
        model = IncomeDomain

    name = factory.Faker("text", max_nb_chars=20).rstrip(".")
    amount = factory.Faker("random_int", min=20000, max=200000)
    max_yearly_growth_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=0.01, max_value=0.5
    )
    min_yearly_growth_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=-0.5, max_value=0
    )
    start_age = factory.Faker("random_int", min=20, max=65)
    owner = factory.SubFactory(AccountDomainFactory)


class LiabilityDomainFactory(factory.Factory):
    """Factory for LiabilityDomain"""

    class Meta:
        model = LiabilityDomain

    name = factory.Faker("text", max_nb_chars=20).rstrip(".")
    principal_amount = factory.Faker("random_int", min=1000, max=1000000)
    interest_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=0.01, max_value=0.2
    )
    start_age = factory.Faker("random_int", min=20, max=65)
    end_age = factory.LazyAttribute(lambda o: o.start_age + 10)
    owner = factory.SubFactory(AccountDomainFactory)


class RiskDomainFactory(factory.Factory):
    """Factory for RiskDomain"""

    class Meta:
        model = RiskDomain

    name = factory.Faker("text", max_nb_chars=20).rstrip(".")
    max_loss = factory.Faker("random_int", min=10000, max=500000)
    min_loss = factory.Faker("random_int", min=5000, max=10000)
    start_age = factory.Faker("random_int", min=20, max=65)
    owner = factory.SubFactory(AccountDomainFactory)


class ScenarioDomainFactory(factory.Factory):
    """Factory for ScenarioDomain"""

    class Meta:
        model = ScenarioDomain

    name = factory.Faker("text", max_nb_chars=20).rstrip(".")
    asset_allocation_percentage = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=0.0, max_value=1.0
    )
    retire_age = factory.Faker("random_int", min=50, max=80)
    owner = factory.SubFactory(AccountDomainFactory)
