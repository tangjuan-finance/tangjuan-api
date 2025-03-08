import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import BaseYearIntervalMixin


class ScenarioSalary(BaseYearIntervalMixin, db.Model):
    left_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("scenario.id"), primary_key=True
    )
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("salary.id"), primary_key=True
    )
    upper_raise_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    lower_raise_rate: so.Mapped[float] = so.mapped_column(sa.Numeric)
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="salary")  # noqa: F821
    salary: so.Mapped["Salary"] = so.relationship(back_populates="scenario")  # noqa: F821
