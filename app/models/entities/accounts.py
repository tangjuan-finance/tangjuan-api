from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from app.models import PrimaryIdMixin, TimestampMixin


class Account(PrimaryIdMixin, TimestampMixin, db.Model):
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    # One-to-Many Ownership
    scenarios: so.WriteOnlyMapped["Scenario"] = so.relationship(back_populates="owner")  # noqa: F821
    expenses: so.WriteOnlyMapped["Expense"] = so.relationship(back_populates="owner")  # noqa: F821
    incomes: so.WriteOnlyMapped["Income"] = so.relationship(back_populates="owner")  # noqa: F821
    assets: so.WriteOnlyMapped["Asset"] = so.relationship(  # noqa: F821
        back_populates="owner"
    )
    liabilities: so.WriteOnlyMapped["Liability"] = so.relationship(  # noqa: F821
        back_populates="owner"
    )
    houses: so.WriteOnlyMapped["House"] = so.relationship(back_populates="owner")  # noqa: F821
    children: so.WriteOnlyMapped["Child"] = so.relationship(back_populates="parent")  # noqa: F821
    risks: so.WriteOnlyMapped["Risk"] = so.relationship(back_populates="owner")  # noqa: F821

    def __repr__(self):
        return "<Account {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"
