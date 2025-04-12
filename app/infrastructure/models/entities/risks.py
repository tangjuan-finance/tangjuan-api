import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.infrastructure.models import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseDescriptionMixin,
    BaseAgeIntervalMixin,
)
from decimal import Decimal


class Risk(
    PrimaryIdMixin, TimestampMixin, BaseDescriptionMixin, BaseAgeIntervalMixin, db.Model
):
    amount: so.Mapped[int] = so.mapped_column(sa.BigInteger)
    probability: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(5, 2))

    # Ownership
    owner_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("account.id", ondelete="CASCADE"), index=True
    )
    owner: so.Mapped["Account"] = so.relationship(back_populates="risks")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioRisk"]] = so.relationship(  # noqa: F821
        back_populates="risk",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Risk or its associations are removed
    )

    def __repr__(self):
        return "<Risk {}>".format(self.id)
