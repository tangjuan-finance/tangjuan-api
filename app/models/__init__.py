import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from .mixins import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseAgeIntervalMixin,
    BaseDescriptionMixin,
    BaseYearlyGrowthRateMixin,
    BaseAmountMixin,
    BaseMemoMixin,
    BaseAgeIntervalOptionalMixin,
)
from .entities import (
    Account,
    Scenario,
    Expense,
    Income,
    House,
    Child,
    Risk,
    Asset,
)
from .associations import (
    ScenarioExpense,
    ScenarioIncome,
    ScenarioAsset,
    ScenarioHouse,
    ScenarioChild,
    ScenarioLiability,
    ScenarioRisk,
)


# Validation Tables
class Age(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    year: so.Mapped[int] = so.mapped_column(sa.SmallInteger)

    def __repr__(self):
        return "<Age {} years>".format(self.year)


# Define __all__ to specify the public interface
__all__ = [
    "Account",
    "Scenario",
    "Expense",
    "Income",
    "House",
    "Child",
    "Risk",
    "Asset",
    "ScenarioExpense",
    "ScenarioIncome",
    "ScenarioAsset",
    "ScenarioHouse",
    "ScenarioChild",
    "ScenarioLiability",
    "ScenarioRisk",
    "PrimaryIdMixin",
    "TimestampMixin",
    "BaseAgeIntervalMixin",
    "BaseDescriptionMixin",
    "BaseYearlyGrowthRateMixin",
    "BaseAmountMixin",
    "BaseMemoMixin",
    "BaseAgeIntervalOptionalMixin",
]
