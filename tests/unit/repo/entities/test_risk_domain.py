from app.repository.entities import RiskRepo
from app.infrastructure.models.entities import Risk
from tests.unit.factories import RiskDomainFactory
import sqlalchemy as sa
from app import db


class TestRiskRepoCase:
    def test_create_risk_domain_through_repo(self):
        # Arrange: Create an risk domain using the factory
        risk = RiskDomainFactory()

        # Act: Save the risk domain using the repo and return the saved entity
        risk_from_repo = RiskRepo.create(risk)
        risk_from_db = db.session.scalar(sa.select(Risk).where(Risk.id == risk.id))

        # Assert: Ensure the values match between the domain object and the saved record
        assert risk_from_repo.id == risk_from_db.id
        assert risk_from_repo.name == risk_from_db.name
        assert risk_from_repo.max_loss == risk_from_db.max_loss
        assert risk_from_repo.min_loss == risk_from_db.min_loss
        assert risk_from_repo.start_age == risk_from_db.start_age
        assert risk_from_repo.owner == risk_from_db.owner
        assert risk_from_repo.created_at == risk_from_db.created_at
        assert risk_from_repo.updated_at == risk_from_db.updated_at

    def test_update_risk_domain_through_repo(self):
        # Arrange: Create an risk domain using the factory
        risk = RiskDomainFactory()
        risk_from_repo = RiskRepo.create(risk)
        updated_name = "Updated Risk Domain"

        # Act: Update the risk domain object (before saving)
        risk_from_repo.name = updated_name

        # Save the updated object through the repository and get the result
        updated_risk = RiskRepo.save(risk_from_repo)

        # Query the database to verify the updated risk record
        risk_from_db = db.session.scalar(
            sa.select(Risk).where(Risk.id == risk_from_repo.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_risk.id == risk_from_db.id
        assert updated_risk.name == risk_from_db.name
        assert updated_risk.created_at == risk_from_db.created_at
        assert updated_risk.updated_at != risk_from_db.updated_at

    def test_get_risk_domain_by_id_through_repo(self):
        # Arrange: Create an risk domain using the factory
        risk = RiskDomainFactory()
        RiskRepo.create(risk)

        # Act: Update the risk domain object (before saving)
        risk_get_by_id = RiskRepo.get_by_id(risk.id)

        # Assert: Ensure the values match between the domain object and the saved record
        assert risk_get_by_id.id == risk.id
        assert risk_get_by_id.name == risk.name

    def test_get_risk_domain_list_through_repo(self):
        # Arrange: Create an risk domain using the factory
        origin_risk_list_length = len(RiskRepo.get_list())

        # Act: Create 5 new risk domains
        for _ in range(5):
            risk = RiskDomainFactory()
            RiskRepo.create(risk)

        # Assert: Ensure the list length is increased by 5
        updated_risk_list_length = len(RiskRepo.get_list())
        assert updated_risk_list_length == (origin_risk_list_length + 5)

    def test_delete_risk_domain_through_repo(self):
        # Arrange: Create an risk domain using the factory
        risk = RiskDomainFactory()
        risk_from_repo = RiskRepo.create(risk)

        # Act: Delete the risk domain object
        RiskRepo.delete(risk_from_repo)

        # Assert: Ensure the risk record is deleted from the database
        assert (
            db.session.scalar(sa.select(Risk).where(Risk.id == risk_from_repo.id))
            is None
        )


class TestRiskDomainCase:
    def test_create_risk_domain(self, default_risk_domain, default_account_domain):
        # Assert
        assert default_risk_domain.name == "Default Risk Domain"
        assert default_risk_domain.max_loss == 100000
        assert default_risk_domain.min_loss == 50000
        assert default_risk_domain.start_age == 20
        assert default_risk_domain.owner == default_account_domain

    def test_factory_risk_domain(self):
        # Arrange
        name = "Default Risk Domain"
        max_loss = 100000
        min_loss = 50000
        start_age = 20

        # Act
        risk = RiskDomainFactory(
            name=name,
            max_loss=max_loss,
            min_loss=min_loss,
            start_age=start_age,
        )

        # Assert
        assert risk.name == name
        assert risk.max_loss == max_loss
        assert risk.min_loss == min_loss
        assert risk.start_age == start_age
