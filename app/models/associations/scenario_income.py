import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import (
    BaseAgeIntervalOptionalMixin,
    TimestampMixin,
    BaseYearlyGrowthRateMixin,
    BaseMemoMixin,
)


class ScenarioIncome(
    BaseAgeIntervalOptionalMixin,
    TimestampMixin,
    BaseYearlyGrowthRateMixin,
    BaseMemoMixin,
    db.Model,
):
    left_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("scenario.id"), primary_key=True
    )
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("income.id"), primary_key=True
    )
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="income")  # noqa: F821
    income: so.Mapped["Income"] = so.relationship(back_populates="scenario")  # noqa: F821
