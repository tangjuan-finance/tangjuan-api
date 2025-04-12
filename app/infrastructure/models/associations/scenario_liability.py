import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from app import db
from app.infrastructure.models import (
    BaseAgeIntervalOptionalMixin,
    TimestampMixin,
    BaseMemoMixin,
)
from decimal import Decimal


class ScenarioLiability(
    BaseAgeIntervalOptionalMixin, TimestampMixin, BaseMemoMixin, db.Model
):
    interest_rate: so.Mapped[Optional[Decimal]] = so.mapped_column(sa.DECIMAL(5, 2))
    allocation_percentage: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(3, 2))

    scenario_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("scenario.id", ondelete="CASCADE"),
        primary_key=True,
    )
    liability_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("liability.id", ondelete="CASCADE"),
        primary_key=True,
    )
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="liability")  # noqa: F821
    liability: so.Mapped["Liability"] = so.relationship(back_populates="scenario")  # noqa: F821
