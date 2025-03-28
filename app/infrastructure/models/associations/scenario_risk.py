import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from app import db
from app.infrastructure.models import (
    BaseAgeIntervalOptionalMixin,
    TimestampMixin,
    BaseMemoMixin,
)


class ScenarioRisk(
    BaseAgeIntervalOptionalMixin, TimestampMixin, BaseMemoMixin, db.Model
):
    max_loss: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger)
    min_loss: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger)

    scenario_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("scenario.id", ondelete="CASCADE"),
        primary_key=True,
    )
    risk_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("risk.id", ondelete="CASCADE"),
        primary_key=True,
    )
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="risk")  # noqa: F821
    risk: so.Mapped["Risk"] = so.relationship(back_populates="scenario")  # noqa: F821
