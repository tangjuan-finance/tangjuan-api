import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.infrastructure.models import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseDescriptionMixin,
)
from decimal import Decimal


class Liability(PrimaryIdMixin, TimestampMixin, BaseDescriptionMixin, db.Model):
    principal_amount: so.Mapped[int] = so.mapped_column(sa.BigInteger)
    interest_rate: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(5, 2))
    start_age: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    # End Age is required, so not use BaseAgeIntervalMixin as other entities did
    end_age: so.Mapped[int] = so.mapped_column(sa.SmallInteger)

    # Ownership
    owner_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("account.id"), index=True, ondelete="CASCADE"
    )
    owner: so.Mapped["Account"] = so.relationship(back_populates="liabilities")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioLiability"]] = so.relationship(  # noqa: F821
        back_populates="liability",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Liability or its associations are removed
    )

    def __repr__(self):
        return "<Liability {}>".format(self.name)
