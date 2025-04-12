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


class Expense(
    PrimaryIdMixin,
    TimestampMixin,
    BaseAgeIntervalMixin,
    BaseYearlyGrowthRateMixin,
    BaseDescriptionMixin,
    BaseAmountMixin,
    db.Model,
):
    # Ownership
    owner_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("account.id", ondelete="CASCADE"), index=True
    )
    owner: so.Mapped["Account"] = so.relationship(back_populates="expenses")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioExpense"]] = so.relationship(  # noqa: F821
        back_populates="expense",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Expense or its associations are removed
    )

    def __repr__(self):
        return "<Expense {}>".format(self.name)
