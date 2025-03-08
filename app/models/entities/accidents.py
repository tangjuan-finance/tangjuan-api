import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import BaseDescriptionMixin


class Accident(BaseDescriptionMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    scenarios: so.WriteOnlyMapped["Scenario"] = so.relationship(  # noqa: F821
        back_populates="accident"
    )
    upper_from_salary_ratio: so.Mapped[float] = so.mapped_column(sa.Numeric)
    lower_from_salary_ratio: so.Mapped[float] = so.mapped_column(sa.Numeric)

    # Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    owner: so.Mapped["User"] = so.relationship(back_populates="accidents")  # noqa: F821

    def __repr__(self):
        return "<Accident {}>".format(self.id)
