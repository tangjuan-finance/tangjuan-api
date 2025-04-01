from app.domain.associations import ScenarioAssetDomain
from app.infrastructure.models import ScenarioAsset, Scenario, Asset
from app import db
import sqlalchemy as sa
from sqlalchemy.orm.exc import NoResultFound


class ScenarioAssetRepo:
    @staticmethod
    def create(assoc: ScenarioAssetDomain) -> ScenarioAssetDomain:
        """Given an Associaiton Domain Object, store it in the database and return the stored object."""
        # Check if the association already exists
        existing_assoc = ScenarioAssetRepo._get_assoc_model_by_cid(
            assoc.scenario_id, assoc.asset_id
        )
        if existing_assoc:
            raise ValueError(
                f"Scenario Asset Record with scenario_id {assoc.scenario_id}, asset_id {assoc.asset_id} already exists!"
            )

        # Check if scenario and asset with given ID existed
        try:
            scenario_model = ScenarioAssetRepo._get_scenario_model_by_id(
                assoc.scenario_id
            )
            asset_model = ScenarioAssetRepo._get_asset_model_by_id(assoc.asset_id)
        except ValueError as e:
            raise ValueError(str(e))

        # Instance with required attr
        # Optional attr would be None, which is set in Domain Definition
        assoc_model = ScenarioAsset(
            scenario_id=scenario_model.id,
            asset_id=asset_model.id,
            max_yearly_return_rate=assoc.max_yearly_return_rate,
            min_yearly_return_rate=assoc.min_yearly_return_rate,
            allocation_percentage=assoc.allocation_percentage,
            start_age=assoc.start_age,
            end_age=assoc.end_age,
            memo=assoc.memo,
        )

        # Save the Asset model to the database
        db.session.add(assoc_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioAssetRepo._map_to_domain(assoc_model)

    @staticmethod
    def save(assoc: ScenarioAssetDomain) -> ScenarioAssetDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get asset_model from database
        existing_assoc = ScenarioAssetRepo._get_assoc_model_by_cid(
            assoc.scenario_id, assoc.asset_id
        )
        if not existing_assoc:
            raise ValueError(
                f"Scenario Asset Record with scenario_id {assoc.scenario_id}, asset_id {assoc.asset_id} not found"
            )
        # As existing_assoc is query by scenario_id and asset_id, both id of existing_assoc would be the same as assoc
        existing_assoc.max_yearly_return_rate = assoc.max_yearly_return_rate
        existing_assoc.min_yearly_return_rate = assoc.min_yearly_return_rate
        existing_assoc.allocation_percentage = assoc.allocation_percentage
        existing_assoc.start_age = assoc.start_age
        existing_assoc.end_age = assoc.end_age
        existing_assoc.memo = assoc.memo

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ScenarioAssetRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_by_id(scenario_id: str, asset_id: str) -> ScenarioAssetDomain | None:
        """Retrieve an asset by ID and return as DomainObject."""
        # Get asset_model from database
        existing_assoc = ScenarioAssetRepo._get_assoc_model_by_cid(
            scenario_id, asset_id
        )

        if not existing_assoc:
            return None

        # Return the domain object with attributes populated from the database
        return ScenarioAssetRepo._map_to_domain(existing_assoc)

    @staticmethod
    def get_list(scenario_id: str) -> list[ScenarioAssetDomain]:
        """Retrieve all assets and return as a list of DomainObjects."""
        assoc_model_list = db.session.scalars(
            sa.select(ScenarioAsset).where((ScenarioAsset.scenario_id == scenario_id))
        ).all()

        return [
            ScenarioAssetRepo._map_to_domain(
                assoc,
            )
            for assoc in assoc_model_list
        ]

    @staticmethod
    def delete_by_id(scenario_id: str, asset_id: str) -> None:
        """Given an asset ID, remove it from the database."""
        # Get asset_model from database
        existing_assoc = ScenarioAssetRepo._get_assoc_model_by_cid(
            scenario_id, asset_id
        )

        if existing_assoc:
            db.session.delete(existing_assoc)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(assoc_model: ScenarioAsset) -> ScenarioAssetDomain:
        """Helper method to map the ScenarioAsset model to a ScenarioAssetDomain object."""
        return ScenarioAssetDomain(
            scenario_id=assoc_model.scenario_id,
            asset_id=assoc_model.asset_id,
            max_yearly_return_rate=assoc_model.max_yearly_return_rate,
            min_yearly_return_rate=assoc_model.min_yearly_return_rate,
            allocation_percentage=assoc_model.allocation_percentage,
            start_age=assoc_model.start_age,
            end_age=assoc_model.end_age,
            memo=assoc_model.memo,
            created_at=assoc_model.created_at,
            updated_at=assoc_model.updated_at,
        )

    @staticmethod
    def _get_assoc_model_by_cid(scenario_id: str, asset_id: str) -> ScenarioAsset:
        assoc = db.session.scalar(
            sa.select(ScenarioAsset).where(
                (ScenarioAsset.scenario_id == scenario_id)
                & (ScenarioAsset.asset_id == asset_id)
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
    def _get_asset_model_by_id(asset_id: str) -> Asset:
        try:
            asset_model = db.session.get_one(Asset, asset_id)
        except NoResultFound:
            raise ValueError("Asset not found!")

        return asset_model
