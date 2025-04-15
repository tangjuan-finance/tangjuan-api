import pytest
from app.domain.entities import ChildSavingAmountEntryDomain
from tests.factory import (
    ChildSavingAmountEntryDomainFactory,
    create_fake_id,
)


class TestChildSavingAmountEntryDomainCase:
    def test_create_child_saving_amount_entry_domain(self):
        # Arrange: Provide params
        name = "Elementary Child Saving Amount Entry"
        start_age = 7
        end_age = 12
        amount = 200000
        child_saving_plan_id = create_fake_id()

        # Act: Create the domain
        child_saving_amount_entry = ChildSavingAmountEntryDomain(
            name=name,
            start_age=start_age,
            end_age=end_age,
            amount=amount,
            child_saving_plan_id=child_saving_plan_id,
        )

        # Assert: Check if the domain get from factory get the same param
        assert isinstance(child_saving_amount_entry.id, str)
        assert len(child_saving_amount_entry.id) == 13
        assert child_saving_amount_entry.name == name
        assert child_saving_amount_entry.start_age == start_age
        assert child_saving_amount_entry.end_age == end_age
        assert child_saving_amount_entry.amount == amount
        assert child_saving_amount_entry.child_saving_plan_id == child_saving_plan_id

    def test_factory_child_saving_amount_entry_domain(self):
        # Arrange: Provide params
        name = "Elementary Child Saving Amount Entry"
        start_age = 7
        end_age = 12
        amount = 200000
        child_saving_plan_id = create_fake_id()

        # Act: Create the domain
        child_saving_amount_entry = ChildSavingAmountEntryDomainFactory(
            name=name,
            start_age=start_age,
            end_age=end_age,
            amount=amount,
            child_saving_plan_id=child_saving_plan_id,
        )

        # Assert: Check if the domain get from factory get the same param
        assert isinstance(child_saving_amount_entry.id, str)
        assert len(child_saving_amount_entry.id) == 13
        assert child_saving_amount_entry.name == name
        assert child_saving_amount_entry.start_age == start_age
        assert child_saving_amount_entry.end_age == end_age
        assert child_saving_amount_entry.amount == amount
        assert child_saving_amount_entry.child_saving_plan_id == child_saving_plan_id

    def test_factory_child_saving_amount_entry_domain_without_plan(self):
        # Arrange: Provide params
        name = "Elementary Child Saving Amount Entry"
        start_age = 7
        end_age = 12
        amount = 200000

        # Assert: Create ChildSavingAmountEntry Object without plan should raise TypeError
        with pytest.raises(TypeError):
            ChildSavingAmountEntryDomain(
                name=name, start_age=start_age, end_age=end_age, amount=amount
            )
