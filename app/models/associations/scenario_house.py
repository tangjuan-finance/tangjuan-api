from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import TimestampMixin, BaseMemoMixin
from decimal import Decimal


class ScenarioHouse(TimestampMixin, BaseMemoMixin, db.Model):
    left_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("scenario.id"), primary_key=True
    )
    right_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("house.id"), primary_key=True
    )

    down_payment: so.Mapped[Optional[int]] = so.mapped_column(sa.BigInteger)
    interest_rate: so.Mapped[Optional[Decimal]] = so.mapped_column(sa.DECIMAL(5, 2))
    loan_term: so.Mapped[Optional[int]] = so.mapped_column(sa.SmallInteger)
    purchase_age: so.Mapped[Optional[int]] = so.mapped_column(sa.SmallInteger)
    sale_age: so.Mapped[Optional[Optional[int]]] = so.mapped_column(sa.SmallInteger)

    scenario: so.Mapped["Scenario"] = so.relationship(back_populates="house")  # noqa: F821
    house: so.Mapped["House"] = so.relationship(back_populates="scenario")  # noqa: F821
