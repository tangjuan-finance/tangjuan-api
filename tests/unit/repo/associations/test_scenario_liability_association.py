from app.repository.associations import ScenarioLiabilityRepo
from app.infrastructure.models.associations import ScenarioLiability
from app.domain.associations import ScenarioLiabilityDomain
import sqlalchemy as sa
from app import db
from decimal import Decimal

from tests.unit.repo.factories import create_liability


class TestLiabilityRepoCase:
    @staticmethod
    def _create_assoc(liability_id, scenario_id, allocation_percentage):
        assoc_domain = ScenarioLiabilityDomain(
            liability_id=liability_id,
            scenario_id=scenario_id,
            allocation_percentage=allocation_percentage,
        )
        return ScenarioLiabilityRepo.create(assoc_domain)

    def test_create_scenario_liability_assoc_through_repo(
        self, new_scenario, new_liability
    ):
        # Arrange: Create an liability and a scenario domain using the factory
        default_interest_rate = Decimal("0.2")
        new_liability.interest_rate = default_interest_rate
        assoc_interest_rate = Decimal("0.7")
        allocation_percentage = Decimal("0.35")

        # Create Assoc Domain
        assoc_domain = ScenarioLiabilityDomain(
            liability_id=new_liability.id,
            scenario_id=new_scenario.id,
            interest_rate=assoc_interest_rate,
            allocation_percentage=allocation_percentage,
        )

        # Act: Save the liability domain to the scenario domain by ScenarioLiabilityRepo, and get the association obj back from database
        scenario_liability_from_repo = ScenarioLiabilityRepo.create(assoc_domain)

        scenario_liability_from_db = db.session.scalars(
            sa.select(ScenarioLiability).where(
                (
                    ScenarioLiability.scenario_id
                    == scenario_liability_from_repo.scenario_id
                )
                & (
                    ScenarioLiability.liability_id
                    == scenario_liability_from_repo.liability_id
                )
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert (
            scenario_liability_from_repo.liability_id
            == scenario_liability_from_db.liability_id
        )
        assert (
            scenario_liability_from_repo.scenario_id
            == scenario_liability_from_db.scenario_id
        )
        assert (
            scenario_liability_from_repo.interest_rate
            == scenario_liability_from_db.interest_rate
        )
        assert (
            scenario_liability_from_repo.allocation_percentage == allocation_percentage
        )
        assert (
            scenario_liability_from_repo.allocation_percentage
            == scenario_liability_from_db.allocation_percentage
        )
        assert scenario_liability_from_repo.interest_rate == assoc_interest_rate

    def test_update_scenario_liability_assoc_through_repo(
        self, new_scenario, new_liability
    ):
        # Arrange: Adding a liability to scenario using the ScenarioLiabilityRepo
        default_interest_rate = Decimal("0.7")
        allocation_percentage = Decimal("0.35")
        assoc_domain = ScenarioLiabilityDomain(
            liability_id=new_liability.id,
            scenario_id=new_scenario.id,
            interest_rate=default_interest_rate,
            allocation_percentage=allocation_percentage,
        )
        scenario_liability_from_repo = ScenarioLiabilityRepo.create(assoc_domain)
        updated_interest_rate = Decimal("0.3")

        # Act: Update the liability domain object (before saving)
        scenario_liability_from_repo.interest_rate = updated_interest_rate

        # Save the updated object through the repository and get the result
        updated_scenario_liability = ScenarioLiabilityRepo.save(
            scenario_liability_from_repo
        )

        # Query the database to verify the updated liability record
        scenario_liability_from_db = db.session.scalars(
            sa.select(ScenarioLiability).where(
                (
                    ScenarioLiability.scenario_id
                    == scenario_liability_from_repo.scenario_id
                )
                & (
                    ScenarioLiability.liability_id
                    == scenario_liability_from_repo.liability_id
                )
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert (
            updated_scenario_liability.liability_id
            == scenario_liability_from_db.liability_id
        )
        assert (
            updated_scenario_liability.scenario_id
            == scenario_liability_from_db.scenario_id
        )
        assert updated_scenario_liability.interest_rate == updated_interest_rate
        assert (
            updated_scenario_liability.interest_rate
            == scenario_liability_from_db.interest_rate
        )
        assert (
            updated_scenario_liability.created_at
            == scenario_liability_from_db.created_at
        )
        assert (
            updated_scenario_liability.updated_at
            == scenario_liability_from_db.updated_at
        )
        # Update_at from updated_liability should be different from the previous liability domain (the one before update)
        assert (
            updated_scenario_liability.updated_at
            > scenario_liability_from_repo.updated_at
        )

    def test_get_scenario_liability_assoc_by_id_through_repo(
        self, new_scenario, new_liability
    ):
        # Arrange: Create an liability domain using the factory
        scenario_liability_from_repo = self._create_assoc(
            liability_id=new_liability.id,
            scenario_id=new_scenario.id,
            allocation_percentage=Decimal("0.35"),
        )

        # Act: Update the liability domain object (before saving)
        scenario_liability_get_by_id = ScenarioLiabilityRepo.get_by_id(
            scenario_id=scenario_liability_from_repo.scenario_id,
            liability_id=scenario_liability_from_repo.liability_id,
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert (
            scenario_liability_get_by_id.scenario_id
            == scenario_liability_from_repo.scenario_id
        )
        assert (
            scenario_liability_get_by_id.liability_id
            == scenario_liability_from_repo.liability_id
        )

    def test_get_scenario_liability_assoc_list_through_repo(
        self, default_account, new_scenario
    ):
        # Arrange: Create an liability domain using the factory
        origin_repo_list_length = len(
            ScenarioLiabilityRepo.get_list(scenario_id=new_scenario.id)
        )

        # Act: Create 5 new liability domains
        for _ in range(5):
            new_liability = create_liability(default_account)
            self._create_assoc(
                liability_id=new_liability.id,
                scenario_id=new_scenario.id,
                allocation_percentage=Decimal("0.35"),
            )

        # Assert: Ensure the list length is increased by 5
        updated_list_length = len(
            ScenarioLiabilityRepo.get_list(scenario_id=new_scenario.id)
        )
        assert updated_list_length == (origin_repo_list_length + 5)

    def test_delete_scenario_liability_assoc_through_repo(
        self, new_scenario, new_liability
    ):
        # Arrange: Create an liability domain using the factory
        scenario_liability_from_repo = self._create_assoc(
            liability_id=new_liability.id,
            scenario_id=new_scenario.id,
            allocation_percentage=Decimal("0.35"),
        )

        # Act: Delete the liability domain object
        ScenarioLiabilityRepo.delete_by_id(
            scenario_id=scenario_liability_from_repo.scenario_id,
            liability_id=scenario_liability_from_repo.liability_id,
        )

        # Assert: Ensure the liability record is deleted from the database
        scenario_liability_from_db = db.session.scalar(
            sa.select(ScenarioLiability).where(
                (
                    ScenarioLiability.scenario_id
                    == scenario_liability_from_repo.scenario_id
                )
                & (
                    ScenarioLiability.liability_id
                    == scenario_liability_from_repo.liability_id
                )
            )
        )
        assert scenario_liability_from_db is None
