import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from .mixins import TimestampMixin, BaseYearIntervalMixin, BaseDescriptionMixin
from .entities import (
    User,
    Scenario,
    Expense,
    Salary,
    Investment,
    House,
    Child,
    Risk,
)
from .associations import (
    ScenarioExpense,
    ScenarioSalary,
    ScenarioInvestment,
    ScenarioHouse,
    ScenarioChild,
)


# Validation Tables
class Age(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    year: so.Mapped[int] = so.mapped_column(sa.SmallInteger)

    def __repr__(self):
        return "<Age {} years>".format(self.year)


# Define __all__ to specify the public interface
__all__ = [
    "User",
    "Scenario",
    "Expense",
    "Salary",
    "Investment",
    "House",
    "Child",
    "Risk",
    "ScenarioExpense",
    "ScenarioSalary",
    "ScenarioInvestment",
    "ScenarioHouse",
    "ScenarioChild",
    "TimestampMixin",
    "BaseYearIntervalMixin",
    "BaseDescriptionMixin",
]
