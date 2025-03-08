from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class ScenarioHouse(db.Model):
    left_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("scenario.id"), primary_key=True
    )
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("house.id"), primary_key=True
    )
    buy_at_age: so.Mapped[int] = so.mapped_column(sa.ForeignKey("age.id"))
    sell_at_age: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("age.id"))
    down_payment: so.Mapped[int] = so.mapped_column(sa.Numeric)
    interest: so.Mapped[int] = so.mapped_column(sa.Numeric)
    loan_term: so.Mapped[int] = so.mapped_column(sa.Integer)
    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="house")  # noqa: F821
    house: so.Mapped["House"] = so.relationship(back_populates="scenario")  # noqa: F821
