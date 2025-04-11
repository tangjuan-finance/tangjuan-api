from app.domain.entities import AssetDomain
from app.infrastructure.models import Asset, Account
from app import db
import sqlalchemy as sa
from .account import AccountRepo
from .base import EntityRepo


class AssetRepo(EntityRepo):
    @staticmethod
    def create(asset: AssetDomain) -> AssetDomain:
        """Given a DomainObject, store it in the database and return the stored object."""
        # Instance with required attr
        asset_model = Asset(
            name=asset.name,
            amount=asset.amount,
            max_yearly_return_rate=asset.max_yearly_return_rate,
            min_yearly_return_rate=asset.min_yearly_return_rate,
            start_age=asset.start_age,
            end_age=asset.end_age,
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            setattr(asset_model, attr, getattr(asset, attr, None))

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == asset.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {asset.owner.id} not found")

        asset_model.owner = owner

        # Save the Asset model to the database
        db.session.add(asset_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return AssetRepo._map_to_domain(asset_model, owner.id)

    @staticmethod
    def save(asset: AssetDomain) -> AssetDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get asset_model from database
        asset_model = db.session.scalar(sa.select(Asset).where(Asset.id == asset.id))
        if not asset_model:
            raise ValueError("Asset not found")

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == asset.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {asset.owner.id} not found")

        # Update Asset Model
        asset_model.name = asset.name
        asset_model.amount = asset.amount
        asset_model.max_yearly_return_rate = asset.max_yearly_return_rate
        asset_model.min_yearly_return_rate = asset.min_yearly_return_rate
        asset_model.start_age = asset.start_age
        asset_model.end_age = asset.end_age
        asset_model.owner = owner

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            origin_attr = getattr(asset_model, attr)
            setattr(asset_model, attr, getattr(asset, attr, origin_attr))

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return AssetRepo._map_to_domain(asset_model, owner.id)

    @staticmethod
    def get_by_id(asset_id: int) -> AssetDomain | None:
        """Retrieve an asset by ID and return as DomainObject."""
        # Get asset_model from database
        asset_model = db.session.scalar(sa.select(Asset).where(Asset.id == asset_id))
        if not asset_model:
            return None

        # Return the domain object with attributes populated from the database
        return AssetRepo._map_to_domain(asset_model, asset_model.owner.id)

    @staticmethod
    def get_list(account_id: str) -> list[AssetDomain]:
        """Retrieve all assets of the account and return as a list of DomainObjects."""
        asset_model_list = db.session.scalars(
            sa.select(Asset).where(Asset.owner_id == account_id)
        ).all()
        return [
            AssetRepo._map_to_domain(asset, asset.owner.id)
            for asset in asset_model_list
        ]

    @staticmethod
    def delete_by_id(asset_id: int) -> None:
        """Given an asset ID, remove it from the database."""
        # Get asset_model from database
        asset_model = db.session.scalar(sa.select(Asset).where(Asset.id == asset_id))
        if asset_model:
            db.session.delete(asset_model)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(asset_model: Asset, owner_id: str) -> AssetDomain:
        """Helper method to map the Asset model to a Domain Object."""
        owner_domain = AccountRepo.get_by_id(owner_id)
        return AssetDomain(
            id=asset_model.id,
            name=asset_model.name,
            amount=asset_model.amount,
            max_yearly_return_rate=asset_model.max_yearly_return_rate,
            min_yearly_return_rate=asset_model.min_yearly_return_rate,
            start_age=asset_model.start_age,
            created_at=asset_model.created_at,
            updated_at=asset_model.updated_at,
            description=asset_model.description,
            end_age=asset_model.end_age,
            owner=owner_domain,
        )
