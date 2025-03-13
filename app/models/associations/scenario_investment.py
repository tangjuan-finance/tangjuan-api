import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import BaseAgeIntervalMixin


class ScenarioInvestment(BaseAgeIntervalMixin, db.Model):
    left_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("scenario.id"), primary_key=True
    )
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("investment.id"), primary_key=True
    )
    upper_return_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    lower_return_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    percentage_from_saving: so.Mapped[float] = so.mapped_column(sa.Numeric)
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="investment")  # noqa: F821
    investment: so.Mapped["Investment"] = so.relationship(back_populates="scenario")  # noqa: F821
