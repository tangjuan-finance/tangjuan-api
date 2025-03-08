import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import TimestampMixin, BaseYearIntervalMixin, BaseDescriptionMixin


class Expense(TimestampMixin, BaseYearIntervalMixin, BaseDescriptionMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[int] = so.mapped_column(sa.Integer)

    # Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    owner: so.Mapped["User"] = so.relationship(back_populates="expenses")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioExpense"]] = so.relationship(  # noqa: F821
        back_populates="expense"
    )

    def __repr__(self):
        return "<Expense {}>".format(self.name)
