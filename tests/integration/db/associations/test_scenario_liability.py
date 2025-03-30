from app import db
from app.infrastructure.models import Scenario, Liability, ScenarioLiability
import sqlalchemy as sa
from ..factories import create_entity
from decimal import Decimal


class TestScenarioLiabilityModelCase:
    def test_default_scenario_liability(self, default_liability, default_scenario):
        # Arrange

        allocation_percentage = Decimal("0.60")

        association = create_entity(
            ScenarioLiability,
            liability=default_liability,
            scenario=default_scenario,
            allocation_percentage=allocation_percentage,
        )
        # Act
        liability_from_db = db.session.scalar(
            sa.select(Liability).where(Liability.id == association.liability_id)
        )
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == association.scenario_id)
        )

        # Assert
        assert association.scenario_id == scenario_from_db.id
        assert association.liability_id == liability_from_db.id
        assert association.scenario == scenario_from_db
        assert association.liability == liability_from_db
        assert association.allocation_percentage == allocation_percentage
        assert association.created_at == association.created_at
        assert association.updated_at == association.updated_at
