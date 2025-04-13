import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.infrastructure.models import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseDescriptionMixin,
)


class Child(PrimaryIdMixin, TimestampMixin, BaseDescriptionMixin, db.Model):
    """
    Represents a child that is linked to a parent and a saving plan.
    """

    birth_age: so.Mapped[int] = so.mapped_column(sa.SmallInteger)

    # Ownership by parent (Account)
    parent_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("account.id", ondelete="CASCADE"), index=True
    )
    parent: so.Mapped["Account"] = so.relationship(back_populates="children")  # noqa: F821

    # Relationship to Scenario (associative entity)
    scenario: so.Mapped[list["ScenarioChild"]] = so.relationship(  # noqa: F821
        back_populates="child",
        passive_deletes=True,
        cascade="all, delete-orphan",  # Ensures association deletion when Child or its associations are removed
    )

    # Many-to-One: Each child belongs to one saving plan
    child_saving_plan_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("child_saving_plan.id"), index=True
    )
    child_saving_plan: so.Mapped["ChildSavingPlan"] = so.relationship(  # noqa: F821
        back_populates="children"
    )

    def __repr__(self):
        return f"<Child {self.name}>"
