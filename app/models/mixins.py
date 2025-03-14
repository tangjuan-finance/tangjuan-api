from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from nanoid import generate
from decimal import Decimal


def generate_nano_id():
    return generate(size=13)  # Generates a 13-char NanoID


class PrimaryIdMixin:
    id: so.Mapped[str] = so.mapped_column(
        sa.String(length=13), primary_key=True, default=generate_nano_id
    )


class TimestampMixin:
    created_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class BaseAgeIntervalMixin:
    start_age: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    end_age: so.Mapped[Optional[int]] = so.mapped_column(sa.SmallInteger)


class BaseAgeIntervalOptionalMixin:
    start_age: so.Mapped[Optional[int]] = so.mapped_column(sa.SmallInteger)
    end_age: so.Mapped[Optional[int]] = so.mapped_column(sa.SmallInteger)


class BaseDescriptionMixin:
    name: so.Mapped[str] = so.mapped_column(sa.String(128))
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)


class BaseYearlyGrowthRateMixin:
    max_yearly_growth_rate: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(5, 2))
    min_yearly_growth_rate: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(5, 2))


class BaseAmountMixin:
    amount: so.Mapped[int] = so.mapped_column(sa.BigInteger)


class BaseMemoMixin:
    memo: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
