from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import TimestampMixin, BaseDescriptionMixin


class Child(TimestampMixin, BaseDescriptionMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    born_at_age: so.Mapped[int] = so.mapped_column(sa.ForeignKey("age.id"))
    independent_year: so.Mapped[Optional[int]] = so.mapped_column(
        sa.ForeignKey("age.id")
    )

    # Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    owner: so.Mapped["User"] = so.relationship(back_populates="children")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioChild"]] = so.relationship(back_populates="child")  # noqa: F821

    def __repr__(self):
        return "<Child {}>".format(self.name)
