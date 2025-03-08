import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models import TimestampMixin, BaseDescriptionMixin


class Scenario(TimestampMixin, BaseDescriptionMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    retire_age: so.Mapped[int] = so.mapped_column(sa.ForeignKey("age.id"), index=True)
    accident_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("accident.id"), index=True
    )
    accident: so.Mapped["Accident"] = so.relationship(back_populates="scenarios")  # noqa: F821
    investment_ratio: so.Mapped[int] = so.mapped_column(sa.Numeric)

    # Ownership
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    owner: so.Mapped["User"] = so.relationship(back_populates="scenarios")  # noqa: F821

    # Many-to-Many Relationship
    expense: so.Mapped[list["ScenarioExpense"]] = so.relationship(  # noqa: F821
        back_populates="scenario"
    )
    salary: so.Mapped[list["ScenarioSalary"]] = so.relationship(  # noqa: F821
        back_populates="scenario"
    )
    investment: so.Mapped[list["ScenarioInvestment"]] = so.relationship(  # noqa: F821
        back_populates="scenario"
    )
    house: so.Mapped[list["ScenarioHouse"]] = so.relationship(back_populates="scenario")  # noqa: F821
    child: so.Mapped[list["ScenarioChild"]] = so.relationship(back_populates="scenario")  # noqa: F821

    def __repr__(self):
        return "<Scenario {}>".format(self.name)
