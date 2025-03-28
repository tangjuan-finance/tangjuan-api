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


class ScenarioAsset(
    BaseAgeIntervalOptionalMixin, TimestampMixin, BaseMemoMixin, db.Model
):
    max_yearly_return_rate: so.Mapped[Optional[Decimal]] = so.mapped_column(
        sa.DECIMAL(5, 2)
    )
    min_yearly_return_rate: so.Mapped[Optional[Decimal]] = so.mapped_column(
        sa.DECIMAL(5, 2)
    )
    allocation_percentage: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(3, 2))

    scenario_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("scenario.id", ondelete="CASCADE"),
        primary_key=True,
    )
    asset_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("asset.id", ondelete="CASCADE"),
        primary_key=True,
    )
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="asset")  # noqa: F821
    asset: so.Mapped["Asset"] = so.relationship(back_populates="scenario")  # noqa: F821
