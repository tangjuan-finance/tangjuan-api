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


class ScenarioRisk(
    BaseAgeIntervalOptionalMixin, TimestampMixin, BaseMemoMixin, db.Model
):
    probability: so.Mapped[Optional[Decimal]] = so.mapped_column(sa.DECIMAL(5, 2))

    scenario_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("scenario.id", ondelete="CASCADE"),
        primary_key=True,
    )
    risk_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("risk.id", ondelete="CASCADE"),
        primary_key=True,
    )
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="risk")  # noqa: F821
    risk: so.Mapped["Risk"] = so.relationship(back_populates="scenario")  # noqa: F821
