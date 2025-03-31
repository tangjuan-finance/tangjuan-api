from app.domain.entities import ScenarioDomain, ResourceDomain
from app.domain.associations import BaseAssociationDomain
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

    @staticmethod
    def add_resource(
        scenario: ScenarioDomain, resource: ResourceDomain, **attrs
    ) -> BaseAssociationDomain:
        """Given Scenario object and a Resource object, store it in the database and return the stored object."""
        from app.mapper.resource_mapper import ResourceMapper

        # Get assoc class
        mapper = ResourceMapper.from_assoc(resource)
        ScenarioResourceAssoc = mapper.assoc_domain_cls

        # Get the correct attribute name for the resource (e.g., "expense", "risk")
        resource_field = mapper.resource_type
        # Create the association with the correct field
        assoc = ScenarioResourceAssoc(
            scenario=scenario,
            **{resource_field: resource},  # Dynamically assign the correct field
            **attrs,
        )

        # Get the repository for storing the association
        ScenarioResourceRepo = mapper.assoc_repo_cls

        # Store the association object to the database
        assoc_from_repo = ScenarioResourceRepo.create(assoc)

        # Add the assoc to the scenario
        scenario._add_association(assoc_from_repo)

        return assoc_from_repo  # Return the stored association

    @staticmethod
    def get_resource_by_id(
        scenario: ScenarioDomain,
        resource_type: ResourceDomain,
        resource_id: str,
    ) -> BaseAssociationDomain:
        """Given Scenario object, Resource Domain, and Resource id, retrieve assoc object from the database."""
        from app.mapper.resource_mapper import ResourceMapper

        # Get assoc class
        mapper = ResourceMapper.from_domain_cls(resource_type)

        # Get the correct attribute name for the resource (e.g., "expense", "risk")
        resource_id_field = f"{mapper.resource_type}_id"

        # Get the association object from repo
        ScenarioResourceRepo = mapper.assoc_repo_cls
        assoc_from_repo = ScenarioResourceRepo.get_by_id(
            scenario_id=scenario.id, **{resource_id_field: resource_id}
        )

        return assoc_from_repo  # Return the retrieved association

    @staticmethod
    def get_resource_list(
        scenario: ScenarioDomain,
        resource_type: ResourceDomain,
    ) -> BaseAssociationDomain:
        """Given Scenario object, Resource Domain, retrieve list of assoc object from the database."""
        from app.mapper.resource_mapper import ResourceMapper

        # Get assoc class
        mapper = ResourceMapper.from_domain_cls(resource_type)

        # Get the list of association object from repo
        ScenarioResourceRepo = mapper.assoc_repo_cls
        assoc_list_from_repo = ScenarioResourceRepo.get_list(scenario_id=scenario.id)

        return assoc_list_from_repo  # Return the retrieved association

    @staticmethod
    def update_resource(
        scenario: ScenarioDomain, resource: ResourceDomain, **attrs
    ) -> BaseAssociationDomain:
        """Given Scenario object and a Resource object, store it in the database and return the stored object."""
        from app.mapper.resource_mapper import ResourceMapper

        # Get assoc class
        mapper = ResourceMapper.from_assoc(resource)

        # Get the correct attribute name for the resource (e.g., "expense", "risk")
        resource_id_field = f"{mapper.resource_type}_id"

        # Get the repository for retrieving the association
        ScenarioResourceRepo = mapper.assoc_repo_cls
        assoc_from_repo = ScenarioResourceRepo.get_by_id(
            scenario_id=scenario.id, **{resource_id_field: resource.id}
        )

        if assoc_from_repo is None:
            raise ValueError(
                f"No Association with scenario_id {scenario.id}, {resource_id_field} {resource.id}"
            )

        # Update the assoc by domain
        updated_assoc = scenario._update_association(assoc_from_repo, **attrs)

        # Save the assoc to the database
        updated_assoc_from_repo = ScenarioResourceRepo.save(updated_assoc)

        return updated_assoc_from_repo  # Return the stored association

    @staticmethod
    def remove_resource(
        scenario: ScenarioDomain,
        resource_type: ResourceDomain,
        resource_id: str,
    ) -> BaseAssociationDomain:
        """Given Scenario object, Resource Domain, and Resource id, retrieve assoc object from the database."""
        from app.mapper.resource_mapper import ResourceMapper

        # Get assoc class
        mapper = ResourceMapper.from_domain_cls(resource_type)

        # Get the correct attribute name for the resource (e.g., "expense", "risk")
        resource_id_field = f"{mapper.resource_type}_id"

        # Delete the association object from repo
        ScenarioResourceRepo = mapper.assoc_repo_cls
        assoc_from_repo = ScenarioResourceRepo.delete_by_id(
            scenario_id=scenario.id, **{resource_id_field: resource_id}
        )

        return assoc_from_repo  # Return the retrieved association
