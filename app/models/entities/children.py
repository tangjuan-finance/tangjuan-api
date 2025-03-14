from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import PrimaryIdMixin, TimestampMixin, BaseDescriptionMixin


class Child(PrimaryIdMixin, TimestampMixin, BaseDescriptionMixin, db.Model):
    birth_age: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    independent_age: so.Mapped[Optional[int]] = so.mapped_column(sa.SmallInteger)

    # Ownership
    parent_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("account.id"), index=True
    )
    parent: so.Mapped["Account"] = so.relationship(back_populates="children")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioChild"]] = so.relationship(back_populates="child")  # noqa: F821

    def __repr__(self):
        return "<Child {}>".format(self.name)
