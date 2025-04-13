# from app.domain.entities import ChildDomain
from tests.factory import (
    ChildSavingAmountEntryDomainFactory,
    ChildSavingPlanDomainFactory,
)


class TestChildSavingAmountEntryDomainCase:
    def test_factory_child_saving_amount_entry_domain(self):
        # Arrange: Provide params
        age = 34
        amount = 200000
        child_saving_plan_id = ChildSavingPlanDomainFactory().id

        # Act: Create the domain
        child_saving_amount_entry = ChildSavingAmountEntryDomainFactory(
            age=age,
            amount=amount,
            child_saving_plan_id=child_saving_plan_id,
        )

        # Assert: Check if the domain get from factory get the same param
        assert child_saving_amount_entry.age == age
        assert child_saving_amount_entry.amount == amount
        assert child_saving_amount_entry.child_saving_plan_id == child_saving_plan_id
