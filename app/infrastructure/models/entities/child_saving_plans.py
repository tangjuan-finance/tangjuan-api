import sqlalchemy.orm as so
from app import db
from app.infrastructure.models import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseDescriptionMixin,
)


class ChildSavingPlan(PrimaryIdMixin, TimestampMixin, BaseDescriptionMixin, db.Model):
    """
    Represents a savings plan for one or more children.
    """

    # One-to-Many: A plan can include multiple children
    children: so.Mapped[list["Child"]] = so.relationship(  # noqa: F821
        back_populates="child_saving_plan",
        cascade="save-update",
        order_by="Child.birth_age",
    )

    # One-to-Many: A plan has specific saving entries for child ages
    child_saving_amount_entries: so.Mapped[list["ChildSavingAmountEntry"]] = (  # noqa: F821
        so.relationship(  # noqa: F821
            back_populates="child_saving_plan",
            cascade="all, delete-orphan",  # Delete all child_saving_amount_entries when child_saving_plan deleted
            passive_deletes=True,
            order_by="ChildSavingAmountEntry.age",
        )
    )

    def __repr__(self):
        return f"<ChildSavingPlan {self.name}>"
