from app.domain.associations import ScenarioChildDomain
from app.infrastructure.models import ScenarioChild, Scenario, Child
from app import db
import sqlalchemy as sa
from sqlalchemy.orm.exc import NoResultFound


class ScenarioChildRepo:
    @staticmethod
    def create(assoc: ScenarioChildDomain) -> ScenarioChildDomain:
        """Given an Associaiton Domain Object, store it in the database and return the stored object."""
        # Check if the association already exists
        existing_assoc = ScenarioChildRepo._get_assoc_model_by_cid(
            assoc.scenario_id, assoc.child_id
        )
        if existing_assoc:
            raise ValueError(
                f"Scenario Child Record with scenario_id {assoc.scenario_id}, child_id {assoc.child_id} already exists!"
            )

        # Check if scenario and child with given ID existed
        try:
            scenario_model = ScenarioChildRepo._get_scenario_model_by_id(
                assoc.scenario_id
            )
            child_model = ScenarioChildRepo._get_child_model_by_id(assoc.child_id)
        except ValueError as e:
            raise ValueError(str(e))

        # Instance with required attr
        # Optional attr would be None, which is set in Domain Definition
        assoc_model = ScenarioChild(
            scenario_id=scenario_model.id,
            child_id=child_model.id,
            birth_age=assoc.birth_age,
            independent_age=assoc.independent_age,
            memo=assoc.memo,
        )

        # Save the Child model to the database
        db.session.add(assoc_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioChildRepo._map_to_domain(assoc_model)

    @staticmethod
    def save(assoc: ScenarioChildDomain) -> ScenarioChildDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get child_model from database
        existing_assoc = ScenarioChildRepo._get_assoc_model_by_cid(
            assoc.scenario_id, assoc.child_id
        )
        if not existing_assoc:
            raise ValueError(
                f"Scenario Child Record with scenario_id {assoc.scenario_id}, child_id {assoc.child_id} not found"
            )
        # As existing_assoc is query by scenario_id and child_id, both id of existing_assoc would be the same as assoc
        existing_assoc.birth_age = assoc.birth_age
        existing_assoc.independent_age = assoc.independent_age
        existing_assoc.memo = assoc.memo

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioChildRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_by_id(scenario_id: str, child_id: str) -> ScenarioChildDomain | None:
        """Retrieve an child by ID and return as DomainObject."""
        # Get child_model from database
        existing_assoc = ScenarioChildRepo._get_assoc_model_by_cid(
            scenario_id, child_id
        )

        if not existing_assoc:
            return None

        # Return the domain object with attributes populated from the database
        return ScenarioChildRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_list(scenario_id: str) -> list[ScenarioChildDomain]:
        """Retrieve all children and return as a list of DomainObjects."""
        assoc_model_list = db.session.scalars(
            sa.select(ScenarioChild).where((ScenarioChild.scenario_id == scenario_id))
        ).all()

        return [
            ScenarioChildRepo._map_to_domain(
                assoc,
            )
            for assoc in assoc_model_list
        ]

    @staticmethod
    def delete_by_id(scenario_id: str, child_id: str) -> None:
        """Given an child ID, remove it from the database."""
        # Get child_model from database
        existing_assoc = ScenarioChildRepo._get_assoc_model_by_cid(
            scenario_id, child_id
        )

        if existing_assoc:
            db.session.delete(existing_assoc)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(assoc_model: ScenarioChild) -> ScenarioChildDomain:
        """Helper method to map the ScenarioChild model to a ScenarioChildDomain object."""
        return ScenarioChildDomain(
            scenario_id=assoc_model.scenario_id,
            child_id=assoc_model.child_id,
            birth_age=assoc_model.birth_age,
            independent_age=assoc_model.independent_age,
            memo=assoc_model.memo,
            created_at=assoc_model.created_at,
            updated_at=assoc_model.updated_at,
        )

    @staticmethod
    def _get_assoc_model_by_cid(scenario_id: str, child_id: str) -> ScenarioChild:
        # Check if scenario existed
        return_scenario_id = ScenarioChildRepo._get_scenario_model_by_id(scenario_id).id

        # Check if child existed
        return_child_id = ScenarioChildRepo._get_child_model_by_id(child_id).id

        # Get assoc by checked scenario and child id
        assoc = db.session.scalar(
            sa.select(ScenarioChild).where(
                (ScenarioChild.scenario_id == return_scenario_id)
                & (ScenarioChild.child_id == return_child_id)
            )
        )
        return assoc

    @staticmethod
    def _get_scenario_model_by_id(scenario_id: str) -> Scenario:
        if not isinstance(scenario_id, str):
            raise TypeError("scenario_id shoud be type str")
        try:
            scenario_model = db.session.get_one(Scenario, scenario_id)
        except NoResultFound:
            raise ValueError("Scenario not found!")

        return scenario_model

    @staticmethod
    def _get_child_model_by_id(child_id: str) -> Child:
        if not isinstance(child_id, str):
            raise TypeError("child_id shoud be type str")
        try:
            child_model = db.session.get_one(Child, child_id)
        except NoResultFound:
            raise ValueError("Child not found!")

        return child_model
