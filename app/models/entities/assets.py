import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from decimal import Decimal
from app.models import (
    PrimaryIdMixin,
    TimestampMixin,
    BaseAgeIntervalMixin,
    BaseDescriptionMixin,
    BaseAmountMixin,
)


class Asset(
    PrimaryIdMixin,
    TimestampMixin,
    BaseAgeIntervalMixin,
    BaseDescriptionMixin,
    BaseAmountMixin,
    db.Model,
):
    max_yearly_growth_rate: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(5, 2))
    min_yearly_growth_rate: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(5, 2))

    # Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("account.id"), index=True)
    owner: so.Mapped["Account"] = so.relationship(back_populates="assets")  # noqa: F821

    # Relationship to Scenario
    scenario: so.Mapped[list["ScenarioAsset"]] = so.relationship(  # noqa: F821
        back_populates="asset"
    )

    def __repr__(self):
        return "<Asset {}>".format(self.name)
