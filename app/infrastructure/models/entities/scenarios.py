import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.infrastructure.models import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseDescriptionMixin,
)
from decimal import Decimal


class Scenario(PrimaryIdMixin, TimestampMixin, BaseDescriptionMixin, db.Model):
    retire_age: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    asset_allocation_percentage: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(3, 2))

    # Ownership
    owner_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("account.id", ondelete="CASCADE"),
        index=True,
    )
    owner: so.Mapped["Account"] = so.relationship(back_populates="scenarios")  # noqa: F821

    # Many-to-Many Relationship
    expense: so.Mapped[list["ScenarioExpense"]] = so.relationship(  # noqa: F821
        back_populates="scenario",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Scenario or its associations are removed
    )
    income: so.Mapped[list["ScenarioIncome"]] = so.relationship(  # noqa: F821
        back_populates="scenario",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Scenario or its associations are removed
    )
    asset: so.Mapped[list["ScenarioAsset"]] = so.relationship(  # noqa: F821
        back_populates="scenario",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Scenario or its associations are removed
    )
    house: so.Mapped[list["ScenarioHouse"]] = so.relationship(  # noqa: F821
        back_populates="scenario",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Scenario or its associations are removed
    )
    child: so.Mapped[list["ScenarioChild"]] = so.relationship(  # noqa: F821
        back_populates="scenario",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Scenario or its associations are removed
    )  # noqa: F821
    risk: so.Mapped[list["ScenarioRisk"]] = so.relationship(  # noqa: F821
        back_populates="scenario",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Scenario or its associations are removed
    )
    liability: so.Mapped[list["ScenarioLiability"]] = so.relationship(  # noqa: F821
        back_populates="scenario",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Scenario or its associations are removed
    )

    def __repr__(self):
        return "<Scenario {}>".format(self.name)
