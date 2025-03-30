from types import MappingProxyType
from app.domain.associations import (
    ScenarioExpenseDomain,
    ScenarioIncomeDomain,
    ScenarioHouseDomain,
    ScenarioChildDomain,
    ScenarioRiskDomain,
    ScenarioAssetDomain,
    ScenarioLiabilityDomain,
)
from app.repository.associations import (
    ScenarioExpenseRepo,
    ScenarioIncomeRepo,
    ScenarioHouseRepo,
    ScenarioChildRepo,
    ScenarioRiskRepo,
    ScenarioAssetRepo,
    ScenarioLiabilityRepo,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities import ResourceDomain


class ResourceMapper:
    _VALID_RESOURCE_TYPES = frozenset(
        {"child", "liability", "expense", "income", "house", "risk", "asset"}
    )

    def __init__(self, resource_type: str):
        if resource_type not in self._VALID_RESOURCE_TYPES:
            raise ValueError(f"Invalid resource type: {resource_type}")
        self._resource_type = resource_type

    @classmethod
    def from_domain(cls, resource: "ResourceDomain"):
        resource_type = type(resource).__name__.replace("Domain", "").lower()

        return ResourceMapper(resource_type)

    @classmethod
    def from_assoc(cls, resource: "ResourceDomain"):
        resource_type = (
            type(resource)
            .__name__.replace("Scenario", "")
            .replace("Domain", "")
            .lower()
        )

        return ResourceMapper(resource_type)

    _COLLECTION_MAPPING = MappingProxyType(
        {
            "child": "children",
            "liability": "liabilities",
            "expense": "expenses",
            "income": "incomes",
            "house": "houses",
            "risk": "risks",
            "asset": "assets",
        }
    )

    _ASSOC_CLS_MAPPING = MappingProxyType(
        {
            "child": ScenarioChildDomain,
            "liability": ScenarioLiabilityDomain,
            "expense": ScenarioExpenseDomain,
            "income": ScenarioIncomeDomain,
            "house": ScenarioHouseDomain,
            "risk": ScenarioRiskDomain,
            "asset": ScenarioAssetDomain,
        }
    )

    _ASSOC_REPO_MAPPING = MappingProxyType(
        {
            "child": ScenarioChildRepo,
            "liability": ScenarioLiabilityRepo,
            "expense": ScenarioExpenseRepo,
            "income": ScenarioIncomeRepo,
            "house": ScenarioHouseRepo,
            "risk": ScenarioRiskRepo,
            "asset": ScenarioAssetRepo,
        }
    )

    @property
    def resource_type(self):
        return self._resource_type

    # Return collection type (resource type in plural)
    @property
    def collection_type(self):
        return self._COLLECTION_MAPPING[self._resource_type]

    @property
    def assoc_domain_cls(self):
        return self._ASSOC_CLS_MAPPING[self._resource_type]

    @property
    def assoc_repo_cls(self):
        return self._ASSOC_REPO_MAPPING[self._resource_type]
