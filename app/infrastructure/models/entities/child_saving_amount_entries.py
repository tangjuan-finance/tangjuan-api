import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from typing import Optional
from app.infrastructure.models import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseAmountMixin,
)


class ChildSavingAmountEntry(PrimaryIdMixin, TimestampMixin, BaseAmountMixin, db.Model):
    """
    Represents a savings amount for a specific age within a saving plan.
    """

    age: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)

    # Many-to-One: Entry belongs to a single saving plan
    child_saving_plan_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("child_saving_plan.id", ondelete="CASCADE"), index=True
    )
    child_saving_plan: so.Mapped["ChildSavingPlan"] = so.relationship(  # noqa: F821
        back_populates="child_saving_amount_entries"
    )

    def __repr__(self):
        return f"<ChildSavingAmountEntry age={self.age} amount={self.amount}>"
