from app.domain.associations import ScenarioRiskDomain
from app.infrastructure.models import ScenarioRisk, Scenario, Risk
from app import db
import sqlalchemy as sa
from sqlalchemy.orm.exc import NoResultFound


class ScenarioRiskRepo:
    @staticmethod
    def create(assoc: ScenarioRiskDomain) -> ScenarioRiskDomain:
        """Given an Associaiton Domain Object, store it in the database and return the stored object."""
        # Check if the association already exists
        existing_assoc = ScenarioRiskRepo._get_assoc_model_by_cid(
            assoc.scenario_id, assoc.risk_id
        )
        if existing_assoc:
            raise ValueError(
                f"Scenario Risk Record with scenario_id {assoc.scenario_id}, risk_id {assoc.risk_id} already exists!"
            )

        # Check if scenario and risk with given ID existed
        try:
            scenario_model = ScenarioRiskRepo._get_scenario_model_by_id(
                assoc.scenario_id
            )
            risk_model = ScenarioRiskRepo._get_risk_model_by_id(assoc.risk_id)
        except ValueError as e:
            raise ValueError(str(e))

        # Instance with required attr
        # Optional attr would be None, which is set in Domain Definition
        assoc_model = ScenarioRisk(
            scenario_id=scenario_model.id,
            risk_id=risk_model.id,
            max_loss=assoc.max_loss,
            min_loss=assoc.min_loss,
            start_age=assoc.start_age,
            end_age=assoc.end_age,
            memo=assoc.memo,
        )

        # Save the Risk model to the database
        db.session.add(assoc_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioRiskRepo._map_to_domain(assoc_model)

    @staticmethod
    def save(assoc: ScenarioRiskDomain) -> ScenarioRiskDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get risk_model from database
        existing_assoc = ScenarioRiskRepo._get_assoc_model_by_cid(
            assoc.scenario_id, assoc.risk_id
        )
        if not existing_assoc:
            raise ValueError(
                f"Scenario Risk Record with scenario_id {assoc.scenario_id}, risk_id {assoc.risk_id} not found"
            )
        # As existing_assoc is query by scenario_id and risk_id, both id of existing_assoc would be the same as assoc
        existing_assoc.max_loss = assoc.max_loss
        existing_assoc.min_loss = assoc.min_loss
        existing_assoc.start_age = assoc.start_age
        existing_assoc.end_age = assoc.end_age
        existing_assoc.memo = assoc.memo

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioRiskRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_by_id(scenario_id: str, risk_id: str) -> ScenarioRiskDomain | None:
        """Retrieve an risk by ID and return as DomainObject."""
        # Get risk_model from database
        existing_assoc = ScenarioRiskRepo._get_assoc_model_by_cid(scenario_id, risk_id)

        if not existing_assoc:
            return None

        # Return the domain object with attributes populated from the database
        return ScenarioRiskRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_list(scenario_id: str) -> list[ScenarioRiskDomain]:
        """Retrieve all risks and return as a list of DomainObjects."""
        assoc_model_list = db.session.scalars(
            sa.select(ScenarioRisk).where((ScenarioRisk.scenario_id == scenario_id))
        ).all()

        return [
            ScenarioRiskRepo._map_to_domain(
                assoc,
            )
            for assoc in assoc_model_list
        ]

    @staticmethod
    def delete_by_id(scenario_id: str, risk_id: str) -> None:
        """Given an risk ID, remove it from the database."""
        # Get risk_model from database
        existing_assoc = ScenarioRiskRepo._get_assoc_model_by_cid(scenario_id, risk_id)

        if existing_assoc:
            db.session.delete(existing_assoc)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(assoc_model: ScenarioRisk) -> ScenarioRiskDomain:
        """Helper method to map the ScenarioRisk model to a ScenarioRiskDomain object."""
        return ScenarioRiskDomain(
            scenario_id=assoc_model.scenario_id,
            risk_id=assoc_model.risk_id,
            max_loss=assoc_model.max_loss,
            min_loss=assoc_model.min_loss,
            start_age=assoc_model.start_age,
            end_age=assoc_model.end_age,
            memo=assoc_model.memo,
            created_at=assoc_model.created_at,
            updated_at=assoc_model.updated_at,
        )

    @staticmethod
    def _get_assoc_model_by_cid(scenario_id: str, risk_id: str) -> ScenarioRisk:
        assoc = db.session.scalar(
            sa.select(ScenarioRisk).where(
                (ScenarioRisk.scenario_id == scenario_id)
                & (ScenarioRisk.risk_id == risk_id)
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
    def _get_risk_model_by_id(risk_id: str) -> Risk:
        try:
            risk_model = db.session.get_one(Risk, risk_id)
        except NoResultFound:
            raise ValueError("Risk not found!")

        return risk_model
