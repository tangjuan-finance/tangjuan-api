from app.domain.associations import ScenarioIncomeDomain
from app.infrastructure.models import ScenarioIncome, Scenario, Income
from app import db
import sqlalchemy as sa
from sqlalchemy.orm.exc import NoResultFound


class ScenarioIncomeRepo:
    @staticmethod
    def create(assoc: ScenarioIncomeDomain) -> ScenarioIncomeDomain:
        """Given an Associaiton Domain Object, store it in the database and return the stored object."""
        # Check if the association already exists
        existing_assoc = ScenarioIncomeRepo._get_assoc_model_by_cid(
            assoc.scenario_id, assoc.income_id
        )
        if existing_assoc:
            raise ValueError(
                f"Scenario Income Record with scenario_id {assoc.scenario_id}, income_id {assoc.income_id} already exists!"
            )

        # Check if scenario and income with given ID existed
        try:
            scenario_model = ScenarioIncomeRepo._get_scenario_model_by_id(
                assoc.scenario_id
            )
            income_model = ScenarioIncomeRepo._get_income_model_by_id(assoc.income_id)
        except ValueError as e:
            raise ValueError(str(e))

        # Instance with required attr
        # Optional attr would be None, which is set in Domain Definition
        assoc_model = ScenarioIncome(
            scenario_id=scenario_model.id,
            income_id=income_model.id,
            max_yearly_growth_rate=assoc.max_yearly_growth_rate,
            min_yearly_growth_rate=assoc.min_yearly_growth_rate,
            start_age=assoc.start_age,
            end_age=assoc.end_age,
            memo=assoc.memo,
        )

        # Save the Income model to the database
        db.session.add(assoc_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioIncomeRepo._map_to_domain(assoc_model)

    @staticmethod
    def save(assoc: ScenarioIncomeDomain) -> ScenarioIncomeDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get income_model from database
        existing_assoc = ScenarioIncomeRepo._get_assoc_model_by_cid(
            assoc.scenario_id, assoc.income_id
        )
        if not existing_assoc:
            raise ValueError(
                f"Scenario Income Record with scenario_id {assoc.scenario_id}, income_id {assoc.income_id} not found"
            )
        # As existing_assoc is query by scenario_id and income_id, both id of existing_assoc would be the same as assoc
        existing_assoc.max_yearly_growth_rate = assoc.max_yearly_growth_rate
        existing_assoc.min_yearly_growth_rate = assoc.min_yearly_growth_rate
        existing_assoc.start_age = assoc.start_age
        existing_assoc.end_age = assoc.end_age
        existing_assoc.memo = assoc.memo

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioIncomeRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_by_id(scenario_id: str, income_id: str) -> ScenarioIncomeDomain | None:
        """Retrieve an income by ID and return as DomainObject."""
        # Get income_model from database
        existing_assoc = ScenarioIncomeRepo._get_assoc_model_by_cid(
            scenario_id, income_id
        )

        if not existing_assoc:
            return None

        # Return the domain object with attributes populated from the database
        return ScenarioIncomeRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_list(scenario_id: str) -> list[ScenarioIncomeDomain]:
        """Retrieve all incomes and return as a list of DomainObjects."""
        assoc_model_list = db.session.scalars(
            sa.select(ScenarioIncome).where((ScenarioIncome.scenario_id == scenario_id))
        ).all()

        return [
            ScenarioIncomeRepo._map_to_domain(
                assoc,
            )
            for assoc in assoc_model_list
        ]

    @staticmethod
    def delete_by_id(scenario_id: str, income_id: str) -> None:
        """Given an income ID, remove it from the database."""
        # Get income_model from database
        existing_assoc = ScenarioIncomeRepo._get_assoc_model_by_cid(
            scenario_id, income_id
        )

        if existing_assoc:
            db.session.delete(existing_assoc)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(assoc_model: ScenarioIncome) -> ScenarioIncomeDomain:
        """Helper method to map the ScenarioIncome model to a ScenarioIncomeDomain object."""
        return ScenarioIncomeDomain(
            scenario_id=assoc_model.scenario_id,
            income_id=assoc_model.income_id,
            max_yearly_growth_rate=assoc_model.max_yearly_growth_rate,
            min_yearly_growth_rate=assoc_model.min_yearly_growth_rate,
            start_age=assoc_model.start_age,
            end_age=assoc_model.end_age,
            memo=assoc_model.memo,
            created_at=assoc_model.created_at,
            updated_at=assoc_model.updated_at,
        )

    @staticmethod
    def _get_assoc_model_by_cid(scenario_id: str, income_id: str) -> ScenarioIncome:
        assoc = db.session.scalar(
            sa.select(ScenarioIncome).where(
                (ScenarioIncome.scenario_id == scenario_id)
                & (ScenarioIncome.income_id == income_id)
            )
        )
        return assoc

    @staticmethod
    def _get_scenario_model_by_id(scenario_id: str) -> Scenario:
        try:
            scenario_model = db.session.get_one(Scenario, scenario_id)
        except NoResultFound:
            raise ValueError("Scenario not found!")

        return scenario_model

    @staticmethod
    def _get_income_model_by_id(income_id: str) -> Income:
        try:
            income_model = db.session.get_one(Income, income_id)
        except NoResultFound:
            raise ValueError("Income not found!")

        return income_model
