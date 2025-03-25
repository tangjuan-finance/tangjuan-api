from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from hashlib import md5
from app.infrastructure.models import PrimaryIdMixin, TimestampMixin


class Account(PrimaryIdMixin, TimestampMixin, db.Model):
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    # One-to-Many Ownership
    scenarios: so.WriteOnlyMapped["Scenario"] = so.relationship(  # noqa: F821
        cascade="all, delete-orphan",
        order_by="Scenario.updated_at",
        passive_deletes=True,
        back_populates="owner",
    )
    expenses: so.WriteOnlyMapped["Expense"] = so.relationship(  # noqa: F821
        cascade="all, delete-orphan",
        order_by="Expense.updated_at",
        passive_deletes=True,
        back_populates="owner",
    )  # noqa: F821
    incomes: so.WriteOnlyMapped["Income"] = so.relationship(  # noqa: F821
        cascade="all, delete-orphan",
        order_by="Income.updated_at",
        passive_deletes=True,
        back_populates="owner",
    )  # noqa: F821
    assets: so.WriteOnlyMapped["Asset"] = so.relationship(  # noqa: F821
        cascade="all, delete-orphan",
        order_by="Asset.updated_at",
        passive_deletes=True,
        back_populates="owner",
    )
    liabilities: so.WriteOnlyMapped["Liability"] = so.relationship(  # noqa: F821
        cascade="all, delete-orphan",
        order_by="Liability.updated_at",
        passive_deletes=True,
        back_populates="owner",
    )
    houses: so.WriteOnlyMapped["House"] = so.relationship(  # noqa: F821
        cascade="all, delete-orphan",
        order_by="House.updated_at",
        passive_deletes=True,
        back_populates="owner",
    )
    children: so.WriteOnlyMapped["Child"] = so.relationship(  # noqa: F821
        cascade="all, delete-orphan",
        order_by="Child.updated_at",
        passive_deletes=True,
        back_populates="parent",
    )
    risks: so.WriteOnlyMapped["Risk"] = so.relationship(  # noqa: F821
        cascade="all, delete-orphan",
        order_by="Risk.updated_at",
        passive_deletes=True,
        back_populates="owner",
    )

    def __repr__(self):
        return "<Account {}>".format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"
