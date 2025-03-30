from types import MappingProxyType
from app.domain.entities import (
    ExpenseDomain,
    IncomeDomain,
    HouseDomain,
    ChildDomain,
    RiskDomain,
    AssetDomain,
    LiabilityDomain,
)
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
from app.infrastructure.models import (
    ScenarioExpense,
    ScenarioIncome,
    ScenarioHouse,
    ScenarioChild,
    ScenarioRisk,
    ScenarioAsset,
    ScenarioLiability,
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
    def from_domain_cls(cls, domain_cls: "ResourceDomain"):
        resource_type = domain_cls.__name__.replace("Domain", "").lower()

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

    @classmethod
    def by_resource_type(cls, resource_type: str):
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

    _RESOURCE_CLS_MAPPING = MappingProxyType(
        {
            "child": ChildDomain,
            "liability": LiabilityDomain,
            "expense": ExpenseDomain,
            "income": IncomeDomain,
            "house": HouseDomain,
            "risk": RiskDomain,
            "asset": AssetDomain,
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

    _ASSOC_MODEL_MAPPING = MappingProxyType(
        {
            "child": ScenarioChild,
            "liability": ScenarioLiability,
            "expense": ScenarioExpense,
            "income": ScenarioIncome,
            "house": ScenarioHouse,
            "risk": ScenarioRisk,
            "asset": ScenarioAsset,
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
    def resource_domain_cls(self):
        return self._RESOURCE_CLS_MAPPING[self._resource_type]

    @property
    def assoc_domain_cls(self):
        return self._ASSOC_CLS_MAPPING[self._resource_type]

    @property
    def assoc_repo_cls(self):
        return self._ASSOC_REPO_MAPPING[self._resource_type]

    @property
    def assoc_model_cls(self):
        return self._ASSOC_MODEL_MAPPING[self._resource_type]
