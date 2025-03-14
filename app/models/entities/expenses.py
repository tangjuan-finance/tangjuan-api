import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import (
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
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("account.id"), index=True)
    owner: so.Mapped["Account"] = so.relationship(back_populates="expenses")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioExpense"]] = so.relationship(  # noqa: F821
        back_populates="expense"
    )

    def __repr__(self):
        return "<Expense {}>".format(self.name)
