from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.infrastructure.models import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseDescriptionMixin,
    BaseAmountMixin,
)
from decimal import Decimal


class House(
    PrimaryIdMixin, TimestampMixin, BaseDescriptionMixin, BaseAmountMixin, db.Model
):
    down_payment: so.Mapped[int] = so.mapped_column(sa.BigInteger)
    interest_rate: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(5, 2))
    loan_term: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    purchase_age: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    sale_age: so.Mapped[Optional[int]] = so.mapped_column(sa.SmallInteger)

    # Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("account.id"), index=True)
    owner: so.Mapped["Account"] = so.relationship(back_populates="houses")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioHouse"]] = so.relationship(back_populates="house")  # noqa: F821

    def __repr__(self):
        return "<House {}>".format(self.name)
