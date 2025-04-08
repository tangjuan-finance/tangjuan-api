from app.domain.associations import ScenarioHouseDomain
from app.infrastructure.models import ScenarioHouse, Scenario, House
from app import db
import sqlalchemy as sa
from sqlalchemy.orm.exc import NoResultFound
from .base import AssociationRepo


class ScenarioHouseRepo(AssociationRepo):
    @staticmethod
    def create(assoc: ScenarioHouseDomain) -> ScenarioHouseDomain:
        """Given an Associaiton Domain Object, store it in the database and return the stored object."""
        # Check if the association already exists
        scenario_id = assoc.scenario_id
        house_id = assoc.house_id
        existing_assoc = ScenarioHouseRepo._get_assoc_model_by_cid(
            scenario_id=scenario_id, house_id=house_id
        )
        if existing_assoc:
            raise ValueError(
                f"Scenario House Record with scenario_id {assoc.scenario_id}, house_id {assoc.house_id} already exists!"
            )

        # Instance with required attr
        # Optional attr would be None, which is set in Domain Definition
        assoc_model = ScenarioHouse(
            scenario_id=scenario_id,
            house_id=house_id,
            down_payment=assoc.down_payment,
            interest_rate=assoc.interest_rate,
            loan_term=assoc.loan_term,
            purchase_age=assoc.purchase_age,
            sale_age=assoc.sale_age,
            memo=assoc.memo,
        )

        # Save the House model to the database
        db.session.add(assoc_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioHouseRepo._map_to_domain(assoc_model)

    @staticmethod
    def save(assoc: ScenarioHouseDomain) -> ScenarioHouseDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get house_model from database
        existing_assoc = ScenarioHouseRepo._get_assoc_model_by_cid(
            assoc.scenario_id, assoc.house_id
        )
        if not existing_assoc:
            raise ValueError(
                f"Scenario House Record with scenario_id {assoc.scenario_id}, house_id {assoc.house_id} not found"
            )
        # As existing_assoc is query by scenario_id and house_id, both id of existing_assoc would be the same as assoc
        existing_assoc.down_payment = assoc.down_payment
        existing_assoc.interest_rate = assoc.interest_rate
        existing_assoc.loan_term = assoc.loan_term
        existing_assoc.purchase_age = assoc.purchase_age
        existing_assoc.sale_age = assoc.sale_age
        existing_assoc.memo = assoc.memo

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioHouseRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_by_id(scenario_id: str, house_id: str) -> ScenarioHouseDomain | None:
        """Retrieve an house by ID and return as DomainObject."""
        # Get house_model from database
        existing_assoc = ScenarioHouseRepo._get_assoc_model_by_cid(
            scenario_id, house_id
        )

        if not existing_assoc:
            return None

        # Return the domain object with attributes populated from the database
        return ScenarioHouseRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_list(scenario_id: str) -> list[ScenarioHouseDomain]:
        """Retrieve all houses and return as a list of DomainObjects."""
        assoc_model_list = db.session.scalars(
            sa.select(ScenarioHouse).where((ScenarioHouse.scenario_id == scenario_id))
        ).all()

        return [
            ScenarioHouseRepo._map_to_domain(
                assoc,
            )
            for assoc in assoc_model_list
        ]

    @staticmethod
    def delete_by_id(scenario_id: str, house_id: str) -> None:
        """Given an house ID, remove it from the database."""
        # Get house_model from database
        existing_assoc = ScenarioHouseRepo._get_assoc_model_by_cid(
            scenario_id, house_id
        )

        if existing_assoc:
            db.session.delete(existing_assoc)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(assoc_model: ScenarioHouse) -> ScenarioHouseDomain:
        """Helper method to map the ScenarioHouse model to a ScenarioHouseDomain object."""
        return ScenarioHouseDomain(
            scenario_id=assoc_model.scenario_id,
            house_id=assoc_model.house_id,
            down_payment=assoc_model.down_payment,
            interest_rate=assoc_model.interest_rate,
            loan_term=assoc_model.loan_term,
            purchase_age=assoc_model.purchase_age,
            sale_age=assoc_model.sale_age,
            memo=assoc_model.memo,
            created_at=assoc_model.created_at,
            updated_at=assoc_model.updated_at,
        )

    @staticmethod
    def _get_assoc_model_by_cid(scenario_id: str, house_id: str) -> ScenarioHouse:
        # Check if scenario existed
        ScenarioHouseRepo._check_if_scenario_existed_by_id(scenario_id)

        # Check if house existed
        ScenarioHouseRepo._check_if_house_existed_by_id(house_id)

        # Get assoc by checked scenario and house id
        assoc = db.session.scalar(
            sa.select(ScenarioHouse).where(
                (ScenarioHouse.scenario_id == scenario_id)
                & (ScenarioHouse.house_id == house_id)
            )
        )
        return assoc

    @staticmethod
    def _check_if_scenario_existed_by_id(scenario_id: str) -> str:
        if not isinstance(scenario_id, str):
            raise TypeError("scenario_id shoud be type str")
        try:
            db.session.get_one(Scenario, scenario_id)
        except NoResultFound:
            raise ValueError("Scenario not found!")

        return f"Scenario {scenario_id} existed."

    @staticmethod
    def _check_if_house_existed_by_id(house_id: str) -> str:
        if not isinstance(house_id, str):
            raise TypeError("house_id shoud be type str")
        try:
            db.session.get_one(House, house_id)
        except NoResultFound:
            raise ValueError("House not found!")

        return f"House {house_id} existed."
