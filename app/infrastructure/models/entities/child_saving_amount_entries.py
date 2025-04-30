import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.infrastructure.models import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseAmountMixin,
    BaseAgeIntervalMixin,
    BaseDescriptionMixin,
)


class ChildSavingAmountEntry(
    PrimaryIdMixin,
    BaseAmountMixin,
    TimestampMixin,
    BaseAgeIntervalMixin,
    BaseDescriptionMixin,
    db.Model,
):
    """
    Represents a savings amount for a specific age within a saving plan.
    """

    # Many-to-One: Entry belongs to a single saving plan
    child_saving_plan_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("child_saving_plan.id", ondelete="CASCADE"), index=True
    )
    child_saving_plan: so.Mapped["ChildSavingPlan"] = so.relationship(  # noqa: F821
        back_populates="child_saving_amount_entries",
    )

    def __repr__(self):
        return f"<ChildSavingAmountEntry start_age={self.start_age} end_age={self.end_age} amount={self.amount}>"
