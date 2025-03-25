import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.infrastructure.models import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseAgeIntervalMixin,
    BaseDescriptionMixin,
    BaseYearlyGrowthRateMixin,
    BaseAmountMixin,
)


class Income(
    PrimaryIdMixin,
    TimestampMixin,
    BaseAgeIntervalMixin,
    BaseYearlyGrowthRateMixin,
    BaseDescriptionMixin,
    BaseAmountMixin,
    db.Model,
):
    # Ownership
    owner_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("account.id", ondelete="CASCADE"), index=True
    )
    owner: so.Mapped["Account"] = so.relationship(back_populates="incomes")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioIncome"]] = so.relationship(  # noqa: F821
        back_populates="income",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Income or its associations are removed
    )

    def __repr__(self):
        return "<Income {}>".format(self.name)
