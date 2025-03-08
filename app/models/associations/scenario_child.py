from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class ScenarioChild(db.Model):
    left_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("scenario.id"), primary_key=True
    )
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("child.id"), primary_key=True
    )
    born_at_age: so.Mapped[int] = so.mapped_column(sa.ForeignKey("age.id"))
    independent_year: so.Mapped[Optional[int]] = so.mapped_column(
        sa.ForeignKey("age.id")
    )
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="child")  # noqa: F821
    child: so.Mapped["Child"] = so.relationship(back_populates="scenario")  # noqa: F821
