import factory
from tests.factory.domain_factory import (
    ScenarioDomainFactory,
    ExpenseDomainFactory,
    IncomeDomainFactory,
    HouseDomainFactory,
    ChildDomainFactory,
    RiskDomainFactory,
    AssetDomainFactory,
    LiabilityDomainFactory,
)

from app.domain.associations import (
    ScenarioExpenseDomain,
    ScenarioIncomeDomain,
    ScenarioHouseDomain,
    ScenarioChildDomain,
    ScenarioRiskDomain,
    ScenarioAssetDomain,
    ScenarioLiabilityDomain,
)
import faker

fake = faker.Faker()


class BaseAssociationDomainFactory(factory.Factory):
    """Abstract Factory for Resource Domain."""

    class Meta:
        abstract = True  # This prevents instantiation without a model

    scenario_id = factory.SubFactory(ScenarioDomainFactory)
    memo = factory.LazyAttribute(
        lambda o: fake.paragraph(nb_sentences=5) if o.optional else None
    )

    class Params:
        optional = False


class ScenarioChildDomainFactory(BaseAssociationDomainFactory, factory.Factory):
    """Factory for ScenarioChildDomain"""

    class Meta:
        model = ScenarioChildDomain

    child_id = factory.SubFactory(ChildDomainFactory)
    birth_age = factory.LazyAttribute(
        lambda o: fake.random_int(min=20, max=50) if o.optional else None
    )
    independent_age = factory.LazyAttribute(
        lambda o: (o.birth_age + fake.random_int(min=20, max=30))
        if o.optional
        else None
    )


class ScenarioAssetDomainFactory(BaseAssociationDomainFactory, factory.Factory):
    """Factory for ScenarioAssetDomain"""

    class Meta:
        model = ScenarioAssetDomain

    asset_id = factory.SubFactory(AssetDomainFactory)
    allocation_percentage = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=0.00, max_value=1
    )
    min_yearly_return_rate = factory.LazyAttribute(
        lambda o: fake.pydecimal(
            left_digits=1, right_digits=2, min_value=-1.0, max_value=0.05
        )
        if o.optional
        else None
    )
    max_yearly_return_rate = factory.LazyAttribute(
        lambda o: (
            o.min_yearly_return_rate
            + fake.pydecimal(left_digits=1, right_digits=2, min_value=0, max_value=0.1)
        )
        if o.optional
        else None
    )
    start_age = factory.LazyAttribute(
        lambda o: fake.random_int(min=20, max=65) if o.optional else None
    )
    end_age = factory.LazyAttribute(
        lambda o: (o.start_age + fake.random_int(min=0, max=30)) if o.optional else None
    )


class ScenarioExpenseDomainFactory(BaseAssociationDomainFactory, factory.Factory):
    """Factory for ScenarioExpenseDomain"""

    class Meta:
        model = ScenarioExpenseDomain

    expense_id = factory.SubFactory(ExpenseDomainFactory)
    min_yearly_growth_rate = factory.LazyAttribute(
        lambda o: fake.pydecimal(
            left_digits=1, right_digits=2, min_value=-0.5, max_value=0
        )
        if o.optional
        else None
    )
    max_yearly_growth_rate = factory.LazyAttribute(
        lambda o: (
            o.min_yearly_growth_rate
            + fake.pydecimal(left_digits=1, right_digits=2, min_value=0, max_value=0.5)
        )
        if o.optional
        else None
    )
    start_age = factory.LazyAttribute(
        lambda o: fake.random_int(min=20, max=65) if o.optional else None
    )
    end_age = factory.LazyAttribute(
        lambda o: (o.start_age + fake.random_int(min=0, max=30)) if o.optional else None
    )


class ScenarioHouseDomainFactory(BaseAssociationDomainFactory, factory.Factory):
    """Factory for ScenarioHouseDomain"""

    class Meta:
        model = ScenarioHouseDomain

    house_id = factory.SubFactory(HouseDomainFactory)
    down_payment = factory.LazyAttribute(
        lambda o: fake.random_int(min=10000, max=500000) if o.optional else None
    )
    interest_rate = factory.LazyAttribute(
        lambda o: fake.pydecimal(
            left_digits=1, right_digits=2, min_value=1.0, max_value=5.0
        )
        if o.optional
        else None
    )
    loan_term = factory.LazyAttribute(
        lambda o: fake.random_int(min=10, max=40) if o.optional else None
    )
    purchase_age = factory.LazyAttribute(
        lambda o: fake.random_int(min=20, max=65) if o.optional else None
    )
    sale_age = factory.LazyAttribute(
        lambda o: (o.purchase_age + fake.random_int(min=0, max=30))
        if o.optional
        else None
    )


class ScenarioIncomeDomainFactory(BaseAssociationDomainFactory, factory.Factory):
    """Factory for ScenarioIncomeDomain"""

    class Meta:
        model = ScenarioIncomeDomain

    income_id = factory.SubFactory(IncomeDomainFactory)
    min_yearly_growth_rate = factory.LazyAttribute(
        lambda o: fake.pydecimal(
            left_digits=1, right_digits=2, min_value=-0.5, max_value=0
        )
        if o.optional
        else None
    )
    max_yearly_growth_rate = factory.LazyAttribute(
        lambda o: (
            o.min_yearly_growth_rate
            + fake.pydecimal(left_digits=1, right_digits=2, min_value=0, max_value=0.5)
        )
        if o.optional
        else None
    )
    start_age = factory.LazyAttribute(
        lambda o: fake.random_int(min=20, max=65) if o.optional else None
    )
    end_age = factory.LazyAttribute(
        lambda o: (o.start_age + fake.random_int(min=0, max=30)) if o.optional else None
    )


class ScenarioLiabilityDomainFactory(BaseAssociationDomainFactory, factory.Factory):
    """Factory for ScenarioLiabilityDomain"""

    class Meta:
        model = ScenarioLiabilityDomain

    liability_id = factory.SubFactory(LiabilityDomainFactory)
    allocation_percentage = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, min_value=0.00, max_value=1
    )
    interest_rate = factory.LazyAttribute(
        lambda o: fake.pydecimal(
            left_digits=1, right_digits=2, min_value=0.01, max_value=0.2
        )
        if o.optional
        else None
    )
    start_age = factory.LazyAttribute(
        lambda o: fake.random_int(min=20, max=65) if o.optional else None
    )
    end_age = factory.LazyAttribute(
        lambda o: (o.start_age + fake.random_int(min=0, max=30)) if o.optional else None
    )


class ScenarioRiskDomainFactory(BaseAssociationDomainFactory, factory.Factory):
    """Factory for ScenarioRiskDomain"""

    class Meta:
        model = ScenarioRiskDomain

    risk_id = factory.SubFactory(RiskDomainFactory)
    min_loss = factory.LazyAttribute(
        lambda o: fake.random_int(min=5000, max=30000) if o.optional else None
    )
    max_loss = factory.LazyAttribute(
        lambda o: (o.min_loss + fake.random_int(min=0, max=500000))
        if o.optional
        else None
    )
    start_age = factory.LazyAttribute(
        lambda o: fake.random_int(min=20, max=65) if o.optional else None
    )
    end_age = factory.LazyAttribute(
        lambda o: (o.start_age + fake.random_int(min=0, max=30)) if o.optional else None
    )
