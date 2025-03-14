import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseDescriptionMixin,
    BaseAgeIntervalMixin,
)


class Risk(
    PrimaryIdMixin, TimestampMixin, BaseDescriptionMixin, BaseAgeIntervalMixin, db.Model
):
    max_loss: so.Mapped[int] = so.mapped_column(sa.BigInteger)
    min_loss: so.Mapped[int] = so.mapped_column(sa.BigInteger)

    # Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("account.id"), index=True)
    owner: so.Mapped["Account"] = so.relationship(back_populates="risks")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioRisk"]] = so.relationship(  # noqa: F821
        back_populates="risk"
    )

    def __repr__(self):
        return "<Risk {}>".format(self.id)
