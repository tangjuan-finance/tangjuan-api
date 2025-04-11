from app.domain.entities import HouseDomain
from app.infrastructure.models import House, Account
from app import db
import sqlalchemy as sa
from .account import AccountRepo
from .base import EntityRepo


class HouseRepo(EntityRepo):
    @staticmethod
    def create(house: HouseDomain) -> HouseDomain:
        """Given a DomainObject, store it in the database and return the stored object."""
        # Instance with required attr
        house_model = House(
            name=house.name,
            amount=house.amount,
            down_payment=house.down_payment,
            interest_rate=house.interest_rate,
            loan_term=house.loan_term,
            purchase_age=house.purchase_age,
            sale_age=house.sale_age,
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            setattr(house_model, attr, getattr(house, attr, None))

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == house.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {house.owner.id} not found")

        house_model.owner = owner

        # Save the House model to the database
        db.session.add(house_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return HouseRepo._map_to_domain(house_model, owner.id)

    @staticmethod
    def save(house: HouseDomain) -> HouseDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get house_model from database
        house_model = db.session.scalar(sa.select(House).where(House.id == house.id))
        if not house_model:
            raise ValueError("House not found")

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == house.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {house.owner.id} not found")

        # Update House Model
        house_model.name = house.name
        house_model.amount = house.amount
        house_model.down_payment = house.down_payment
        house_model.interest_rate = house.interest_rate
        house_model.loan_term = house.loan_term
        house_model.purchase_age = house.purchase_age
        house_model.sale_age = house.sale_age
        house_model.owner = owner

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            origin_attr = getattr(house_model, attr)
            setattr(house_model, attr, getattr(house, attr, origin_attr))

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return HouseRepo._map_to_domain(house_model, owner.id)

    @staticmethod
    def get_by_id(house_id: int) -> HouseDomain | None:
        """Retrieve an house by ID and return as DomainObject."""
        # Get house_model from database
        house_model = db.session.scalar(sa.select(House).where(House.id == house_id))
        if not house_model:
            return None

        # Return the domain object with attributes populated from the database
        return HouseRepo._map_to_domain(house_model, house_model.owner.id)

    @staticmethod
    def get_list(account_id: str) -> list[HouseDomain]:
        """Retrieve all houses of the account and return as a list of DomainObjects."""
        house_model_list = db.session.scalars(
            sa.select(House).where(House.owner_id == account_id)
        ).all()
        return [
            HouseRepo._map_to_domain(house, house.owner.id)
            for house in house_model_list
        ]

    @staticmethod
    def delete_by_id(house_id: int) -> None:
        """Given an house ID, remove it from the database."""
        # Get house_model from database
        house_model = db.session.scalar(sa.select(House).where(House.id == house_id))
        if house_model:
            db.session.delete(house_model)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(house_model: House, owner_id: str) -> HouseDomain:
        """Helper method to map the House model to a Domain Object."""
        owner_domain = AccountRepo.get_by_id(owner_id)
        return HouseDomain(
            id=house_model.id,
            name=house_model.name,
            amount=house_model.amount,
            down_payment=house_model.down_payment,
            interest_rate=house_model.interest_rate,
            loan_term=house_model.loan_term,
            purchase_age=house_model.purchase_age,
            created_at=house_model.created_at,
            updated_at=house_model.updated_at,
            description=house_model.description,
            sale_age=house_model.sale_age,
            owner=owner_domain,
        )
