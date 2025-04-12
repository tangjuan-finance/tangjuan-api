from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.infrastructure.models import TimestampMixin, BaseMemoMixin


class ScenarioChild(TimestampMixin, BaseMemoMixin, db.Model):
    scenario_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("scenario.id", ondelete="CASCADE"),
        primary_key=True,
    )
    child_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("child.id", ondelete="CASCADE"),
        primary_key=True,
    )
    birth_age: so.Mapped[Optional[int]] = so.mapped_column(sa.SmallInteger)
    independent_age: so.Mapped[Optional[int]] = so.mapped_column(sa.SmallInteger)
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="child")  # noqa: F821
    child: so.Mapped["Child"] = so.relationship(back_populates="scenario")  # noqa: F821
