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
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from nanoid import generate
import faker

fake = faker.Faker()


class IdDomainFactory(factory.Factory):
    """Abstract Factory to add an ID field."""

    class Meta:
        abstract = True  # This prevents instantiation without a model

    id = factory.LazyFunction(lambda: generate(size=13))


class ResourceDomainFactory(IdDomainFactory, factory.Factory):
    """Abstract Factory to add an optional decription field."""

    class Meta:
        abstract = True  # This prevents instantiation without a model

    description = factory.LazyAttribute(
        lambda o: fake.paragraph(nb_sentences=5) if o.optional else None
    )

    class Params:
        optional = False


class AccountDomainFactory(IdDomainFactory, factory.Factory):
    """Factory for AccountDomain"""

    class Meta:
        model = AccountDomain

    name = factory.Faker("user_name")
    email = factory.Faker("email")

    @factory.lazy_attribute
    def password_hash(self):
        password_hash = generate_password_hash(fake.password(length=12))
        return password_hash

    @factory.lazy_attribute
    def last_seen(self):
        last_seen = datetime.now(timezone.utc)
        return last_seen


class ChildDomainFactory(ResourceDomainFactory, factory.Factory):
    """Factory for ChildDomain"""

    class Meta:
        model = ChildDomain

    name = factory.Faker("text", max_nb_chars=20)
    birth_age = factory.Faker("random_int", min=20, max=50)
    independent_age = factory.LazyAttribute(
        lambda o: o.birth_age + fake.random_int(min=20, max=30)
    )
    parent = factory.SubFactory(AccountDomainFactory)


class AssetDomainFactory(ResourceDomainFactory, factory.Factory):
    """Factory for AssetDomain"""

    class Meta:
        model = AssetDomain

    name = factory.Faker("text", max_nb_chars=20)
    amount = factory.Faker("random_int", min=10000, max=1000000)
    min_yearly_return_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=-1.0, max_value=0.05
    )
    max_yearly_return_rate = factory.LazyAttribute(
        lambda o: o.min_yearly_return_rate
        + fake.pydecimal(left_digits=1, right_digits=2, min_value=0, max_value=0.1)
    )
    start_age = factory.Faker("random_int", min=20, max=65)
    end_age = factory.LazyAttribute(
        lambda o: o.start_age + fake.random_int(min=0, max=30)
    )
    owner = factory.SubFactory(AccountDomainFactory)


class ExpenseDomainFactory(ResourceDomainFactory, factory.Factory):
    """Factory for ExpenseDomain"""

    class Meta:
        model = ExpenseDomain

    name = factory.Faker("text", max_nb_chars=20)
    amount = factory.Faker("random_int", min=1000, max=100000)
    min_yearly_growth_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=-0.5, max_value=0
    )
    max_yearly_growth_rate = factory.LazyAttribute(
        lambda o: o.min_yearly_growth_rate
        + fake.pydecimal(left_digits=1, right_digits=2, min_value=0, max_value=0.5)
    )
    start_age = factory.Faker("random_int", min=20, max=65)
    end_age = factory.LazyAttribute(
        lambda o: o.start_age + fake.random_int(min=0, max=30)
    )
    owner = factory.SubFactory(AccountDomainFactory)


class HouseDomainFactory(ResourceDomainFactory, factory.Factory):
    """Factory for HouseDomain"""

    class Meta:
        model = HouseDomain

    name = factory.Faker("text", max_nb_chars=20)
    amount = factory.Faker("random_int", min=100000, max=50000000)
    down_payment = factory.Faker("random_int", min=10000, max=500000)
    interest_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=1.0, max_value=5.0
    )
    loan_term = factory.Faker("random_int", min=10, max=40)
    purchase_age = factory.Faker("random_int", min=20, max=65)
    sale_age = factory.LazyAttribute(
        lambda o: o.purchase_age + fake.random_int(min=0, max=30)
    )
    owner = factory.SubFactory(AccountDomainFactory)


class IncomeDomainFactory(ResourceDomainFactory, factory.Factory):
    """Factory for IncomeDomain"""

    class Meta:
        model = IncomeDomain

    name = factory.Faker("text", max_nb_chars=20)
    amount = factory.Faker("random_int", min=20000, max=200000)
    min_yearly_growth_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=-0.5, max_value=0
    )
    max_yearly_growth_rate = factory.LazyAttribute(
        lambda o: o.min_yearly_growth_rate
        + fake.pydecimal(left_digits=1, right_digits=2, min_value=0, max_value=0.5)
    )
    start_age = factory.Faker("random_int", min=20, max=65)
    end_age = factory.LazyAttribute(
        lambda o: o.start_age + fake.random_int(min=0, max=30)
    )
    owner = factory.SubFactory(AccountDomainFactory)


class LiabilityDomainFactory(ResourceDomainFactory, factory.Factory):
    """Factory for LiabilityDomain"""

    class Meta:
        model = LiabilityDomain

    name = factory.Faker("text", max_nb_chars=20)
    principal_amount = factory.Faker("random_int", min=1000, max=1000000)
    interest_rate = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=0.01, max_value=0.2
    )
    start_age = factory.Faker("random_int", min=20, max=65)
    end_age = factory.LazyAttribute(
        lambda o: o.start_age + fake.random_int(min=0, max=30)
    )
    owner = factory.SubFactory(AccountDomainFactory)


class RiskDomainFactory(ResourceDomainFactory, factory.Factory):
    """Factory for RiskDomain"""

    class Meta:
        model = RiskDomain

    name = factory.Faker("text", max_nb_chars=20)
    amount = factory.Faker("random_int", min=0, max=20000)
    probability = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=0, max_value=0.8
    )
    start_age = factory.Faker("random_int", min=20, max=65)
    end_age = factory.LazyAttribute(
        lambda o: o.start_age + fake.random_int(min=0, max=30)
    )
    owner = factory.SubFactory(AccountDomainFactory)


class ScenarioDomainFactory(ResourceDomainFactory, factory.Factory):
    """Factory for ScenarioDomain"""

    class Meta:
        model = ScenarioDomain

    name = factory.Faker("text", max_nb_chars=20)
    asset_allocation_percentage = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=0.0, max_value=1.0
    )
    retire_age = factory.Faker("random_int", min=50, max=80)
    owner = factory.SubFactory(AccountDomainFactory)
