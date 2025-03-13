import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import BaseAgeIntervalMixin


class ScenarioExpense(BaseAgeIntervalMixin, db.Model):
    left_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("scenario.id"), primary_key=True
    )
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("expense.id"), primary_key=True
    )
    upper_raise_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    lower_raise_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="expense")  # noqa: F821
    expense: so.Mapped["Expense"] = so.relationship(back_populates="scenario")  # noqa: F821
