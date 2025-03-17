# from app.domain.entities import ChildDomain


class TestChildDomainCase:
    def test_create_child_domain(default_child_domain, default_account_domain):
        # Assert
        assert default_child_domain.name == "Default Child Domain"
        assert default_child_domain.birth_age == 34
        assert default_child_domain.independent_age == 56
        assert default_child_domain.owner_id == default_account_domain.id
