from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so


class TimestampMixin:
    created: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class BaseYearIntervalMixin:
    start_year: so.Mapped[int] = so.mapped_column(sa.ForeignKey("age.id"))
    end_year: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("age.id"))


class BaseDescriptionMixin:
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
