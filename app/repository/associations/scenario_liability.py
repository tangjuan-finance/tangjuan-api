from app.domain.associations import ScenarioLiabilityDomain
from app.domain.entities import ScenarioDomain, LiabilityDomain
from app.infrastructure.models import ScenarioLiability, Scenario, Liability
from app.repository.entities import ScenarioRepo, LiabilityRepo
from app import db
import sqlalchemy as sa
from sqlalchemy.orm.exc import NoResultFound


class ScenarioLiabilityRepo:
    @staticmethod
    def create(assoc: ScenarioLiabilityDomain) -> ScenarioLiabilityDomain:
        """Given an Associaiton Domain Object, store it in the database and return the stored object."""
        # Check if the association already exists
        existing_assoc = ScenarioLiabilityRepo._get_assoc_model_by_cid(
            assoc.scenario.id, assoc.liability.id
        )
        if existing_assoc:
            raise ValueError(
                f"Scenario Liability Record with scenario_id {assoc.scenario.id}, liability_id {assoc.liability.id} already exists!"
            )

        try:
            scenario_model = ScenarioLiabilityRepo._get_scenario_model_by_id(
                assoc.scenario.id
            )
            liability_model = ScenarioLiabilityRepo._get_liability_model_by_id(
                assoc.liability.id
            )
        except ValueError as e:
            raise ValueError(str(e))

        # Instance with required attr
        # Optional attr would be None, which is set in Domain Definition
        assoc_model = ScenarioLiability(
            scenario=scenario_model,
            liability=liability_model,
            interest_rate=assoc.interest_rate,
            allocation_percentage=assoc.allocation_percentage,
            start_age=assoc.start_age,
            end_age=assoc.end_age,
            memo=assoc.memo,
        )

        # Save the Liability model to the database
        db.session.add(assoc_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioLiabilityRepo._map_to_domain(
            assoc_model, assoc.scenario, assoc.liability
        )

    @staticmethod
    def save(assoc: ScenarioLiabilityDomain) -> ScenarioLiabilityDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get liability_model from database
        existing_assoc = ScenarioLiabilityRepo._get_assoc_model_by_cid(
            assoc.scenario.id, assoc.liability.id
        )
        if not existing_assoc:
            raise ValueError(
                f"Scenario Liability Record with scenario_id {assoc.scenario.id}, liability_id {assoc.liability.id} not found"
            )
        # As existing_assoc is query by scenario.id and liability.id, both id of existing_assoc would be the same as assoc
        existing_assoc.interest_rate = assoc.interest_rate
        existing_assoc.allocation_percentage = assoc.allocation_percentage
        existing_assoc.start_age = assoc.start_age
        existing_assoc.end_age = assoc.end_age
        existing_assoc.memo = assoc.memo

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioLiabilityRepo._map_to_domain(
            existing_assoc, assoc.scenario, assoc.liability
        )

    @staticmethod
    def get_by_id(
        scenario_id: str, liability_id: str
    ) -> ScenarioLiabilityDomain | None:
        """Retrieve an liability by ID and return as DomainObject."""
        # Get liability_model from database
        existing_assoc = ScenarioLiabilityRepo._get_assoc_model_by_cid(
            scenario_id, liability_id
        )

        if not existing_assoc:
            return None

        scenario_domain = ScenarioRepo.get_by_id(existing_assoc.scenario_id)
        liability_domain = LiabilityRepo.get_by_id(existing_assoc.liability_id)

        # Return the domain object with attributes populated from the database
        return ScenarioLiabilityRepo._map_to_domain(
            existing_assoc, scenario_domain, liability_domain
        )

    @staticmethod
    def get_list() -> list[ScenarioLiabilityDomain]:
        """Retrieve all liabilitys and return as a list of DomainObjects."""
        assoc_model_list = db.session.scalars(sa.select(ScenarioLiability)).all()

        return [
            ScenarioLiabilityRepo._map_to_domain(
                assoc,
                ScenarioRepo.get_by_id(assoc.scenario_id),
                LiabilityRepo.get_by_id(assoc.liability_id),
            )
            for assoc in assoc_model_list
        ]

    @staticmethod
    def delete_by_id(scenario_id: str, liability_id: str) -> None:
        """Given an liability ID, remove it from the database."""
        # Get liability_model from database
        existing_assoc = ScenarioLiabilityRepo._get_assoc_model_by_cid(
            scenario_id, liability_id
        )

        if existing_assoc:
            db.session.delete(existing_assoc)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(
        assoc_model: ScenarioLiability,
        scenario: ScenarioDomain,
        liability: LiabilityDomain,
    ) -> ScenarioLiabilityDomain:
        """Helper method to map the ScenarioLiability model to a ScenarioLiabilityDomain object."""
        return ScenarioLiabilityDomain(
            scenario=scenario,
            liability=liability,
            interest_rate=assoc_model.interest_rate,
            allocation_percentage=assoc_model.allocation_percentage,
            start_age=assoc_model.start_age,
            end_age=assoc_model.end_age,
            memo=assoc_model.memo,
            created_at=assoc_model.created_at,
            updated_at=assoc_model.updated_at,
        )

    @staticmethod
    def _get_assoc_model_by_cid(
        scenario_id: str, liability_id: str
    ) -> ScenarioLiability:
        assoc = db.session.scalar(
            sa.select(ScenarioLiability).where(
                (ScenarioLiability.scenario_id == scenario_id)
                & (ScenarioLiability.liability_id == liability_id)
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
    def _get_liability_model_by_id(liability_id: str) -> Liability:
        try:
            liability_model = db.session.get_one(Liability, liability_id)
        except NoResultFound:
            raise ValueError("Liability not found!")

        return liability_model
