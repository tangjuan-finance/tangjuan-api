from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import TimestampMixin, BaseDescriptionMixin


class House(TimestampMixin, BaseDescriptionMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[int] = so.mapped_column(sa.Integer)
    down_payment: so.Mapped[int] = so.mapped_column(sa.Numeric)
    interest: so.Mapped[int] = so.mapped_column(sa.Numeric)
    loan_term: so.Mapped[int] = so.mapped_column(sa.Integer)
    buy_at_age: so.Mapped[int] = so.mapped_column(sa.ForeignKey("age.id"))
    sell_at_age: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("age.id"))

    # Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    owner: so.Mapped["User"] = so.relationship(back_populates="houses")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioHouse"]] = so.relationship(back_populates="house")  # noqa: F821

    def __repr__(self):
        return "<House {}>".format(self.name)
