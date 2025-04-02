from app.domain.entities import ScenarioDomain
from app.infrastructure.models import Scenario, Account
from app import db
import sqlalchemy as sa
from .account import AccountRepo


class ScenarioRepo:
    @staticmethod
    def create(scenario: ScenarioDomain) -> ScenarioDomain:
        """Given a DomainObject, store it in the database and return the stored object."""
        # Instance with required attr
        scenario_model = Scenario(
            name=scenario.name,
            asset_allocation_percentage=scenario.asset_allocation_percentage,
            retire_age=scenario.retire_age,
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            setattr(scenario_model, attr, getattr(scenario, attr, None))

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == scenario.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {scenario.owner.id} not found")

        scenario_model.owner = owner

        # Save the Scenario model to the database
        db.session.add(scenario_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioRepo._map_to_domain(scenario_model, owner.id)

    @staticmethod
    def save(scenario: ScenarioDomain) -> ScenarioDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get scenario_model from database
        scenario_model = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == scenario.id)
        )
        if not scenario_model:
            raise ValueError("Scenario not found")

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == scenario.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {scenario.owner.id} not found")

        # Update Scenario Model
        scenario_model.name = scenario.name
        scenario_model.asset_allocation_percentage = (
            scenario.asset_allocation_percentage
        )
        scenario_model.retire_age = scenario.retire_age
        scenario_model.owner = owner

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            origin_attr = getattr(scenario_model, attr)
            setattr(scenario_model, attr, getattr(scenario, attr, origin_attr))

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioRepo._map_to_domain(scenario_model, owner.id)

    @staticmethod
    def get_by_id(scenario_id: int) -> ScenarioDomain | None:
        """Retrieve an scenario by ID and return as DomainObject."""
        # Get scenario_model from database
        scenario_model = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == scenario_id)
        )
        if not scenario_model:
            return None

        # Return the domain object with attributes populated from the database
        return ScenarioRepo._map_to_domain(scenario_model, scenario_model.owner.id)

    @staticmethod
    def get_list(account_id: str) -> list[ScenarioDomain]:
        """Retrieve all scenarios of the account and return as a list of DomainObjects."""
        scenario_model_list = db.session.scalars(
            sa.select(Scenario).where(Scenario.owner_id == account_id)
        ).all()
        return [
            ScenarioRepo._map_to_domain(scenario, scenario.owner.id)
            for scenario in scenario_model_list
        ]

    @staticmethod
    def delete_by_id(scenario_id: int) -> None:
        """Given an scenario ID, remove it from the database."""
        # Get scenario_model from database
        scenario_model = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == scenario_id)
        )
        if scenario_model:
            db.session.delete(scenario_model)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(scenario_model: Scenario, owner_id: str) -> ScenarioDomain:
        """Helper method to map the Scenario model to a Domain Object."""
        owner_domain = AccountRepo.get_by_id(owner_id)
        return ScenarioDomain(
            id=scenario_model.id,
            name=scenario_model.name,
            asset_allocation_percentage=scenario_model.asset_allocation_percentage,
            retire_age=scenario_model.retire_age,
            created_at=scenario_model.created_at,
            updated_at=scenario_model.updated_at,
            description=scenario_model.description,
            owner=owner_domain,
        )
