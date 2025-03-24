from app.repository.entities import ChildRepo
from app.infrastructure.models.entities import Child
from tests.unit.factories import ChildDomainFactory
import sqlalchemy as sa
from app import db


class TestChildRepoCase:
    def test_create_child_domain_through_repo(self):
        # Arrange: Create an child domain using the factory
        child = ChildDomainFactory()

        # Act: Save the child domain using the repo and return the saved entity
        child_from_repo = ChildRepo.create(child)
        child_from_db = db.session.scalar(sa.select(Child).where(Child.id == child.id))

        # Assert: Ensure the values match between the domain object and the saved record
        assert child_from_repo.id == child_from_db.id
        assert child_from_repo.name == child_from_db.name
        assert child_from_repo.birth_age == child_from_db.birth_age
        assert child_from_repo.independent_age == child_from_db.independent_age
        assert child_from_repo.parent == child_from_db.parent
        assert child_from_repo.created_at == child_from_db.created_at
        assert child_from_repo.updated_at == child_from_db.updated_at

    def test_update_child_domain_through_repo(self):
        # Arrange: Create an child domain using the factory
        child = ChildDomainFactory()
        child_from_repo = ChildRepo.create(child)
        updated_name = "Updated Child Domain"

        # Act: Update the child domain object (before saving)
        child_from_repo.name = updated_name

        # Save the updated object through the repository and get the result
        updated_child = ChildRepo.save(child_from_repo)

        # Query the database to verify the updated child record
        child_from_db = db.session.scalar(
            sa.select(Child).where(Child.id == child_from_repo.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_child.id == child_from_db.id
        assert updated_child.name == child_from_db.name
        assert updated_child.created_at == child_from_db.created_at
        assert updated_child.updated_at != child_from_db.updated_at

    def test_get_child_domain_by_id_through_repo(self):
        # Arrange: Create an child domain using the factory
        child = ChildDomainFactory()
        ChildRepo.create(child)

        # Act: Update the child domain object (before saving)
        child_get_by_id = ChildRepo.get_by_id(child.id)

        # Assert: Ensure the values match between the domain object and the saved record
        assert child_get_by_id.id == child.id
        assert child_get_by_id.name == child.name

    def test_get_child_domain_list_through_repo(self):
        # Arrange: Create an child domain using the factory
        origin_child_list_length = len(ChildRepo.get_list())

        # Act: Create 5 new child domains
        for _ in range(5):
            child = ChildDomainFactory()
            ChildRepo.create(child)

        # Assert: Ensure the list length is increased by 5
        updated_child_list_length = len(ChildRepo.get_list())
        assert updated_child_list_length == (origin_child_list_length + 5)

    def test_delete_child_domain_through_repo(self):
        # Arrange: Create an child domain using the factory
        child = ChildDomainFactory()
        child_from_repo = ChildRepo.create(child)

        # Act: Delete the child domain object
        ChildRepo.delete(child_from_repo)

        # Assert: Ensure the child record is deleted from the database
        assert (
            db.session.scalar(sa.select(Child).where(Child.id == child_from_repo.id))
            is None
        )
