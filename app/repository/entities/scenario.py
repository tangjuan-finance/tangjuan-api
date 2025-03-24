from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from .base import EntityRepo
from types import MappingProxyType


if TYPE_CHECKING:
    from .account import AccountRepo
    from ..associations import (
        ScenarioExpenseRepo,
        ScenarioIncomeRepo,
        ScenarioHouseRepo,
        ScenarioChildRepo,
        ScenarioRiskRepo,
        ScenarioAssetRepo,
        ScenarioLiabilityRepo,
    )


@dataclass(kw_only=True)
class ScenarioRepo(EntityRepo):
    owner: "AccountRepo"
    name: str
    asset_allocation_percentage: Decimal
    retire_age: int
    description: Optional[str] = None

    # Resource collections
    expenses: List["ScenarioExpenseRepo"] = field(default_factory=list)
    incomes: List["ScenarioIncomeRepo"] = field(default_factory=list)
    houses: List["ScenarioHouseRepo"] = field(default_factory=list)
    children: List["ScenarioChildRepo"] = field(default_factory=list)
    risks: List["ScenarioRiskRepo"] = field(default_factory=list)
    assets: List["ScenarioAssetRepo"] = field(default_factory=list)
    liabilities: List["ScenarioLiabilityRepo"] = field(default_factory=list)

    _VALID_RESOURCE_TYPES = frozenset(
        {"child", "liability", "expense", "income", "house", "risk", "asset"}
    )
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

    def _get_resource_type(self, obj) -> str:
        """Extracts the resource type from the given object."""
        resource_type = (
            type(obj).__name__.replace("Scenario", "").replace("Repo", "").lower()
        )
        if resource_type not in self._VALID_RESOURCE_TYPES:
            raise ValueError(f"Invalid resource type: {resource_type}")
        return resource_type

    def _get_collection(self, resource_type) -> str:
        """Get collection by mapping a resource type to its corresponding collection name."""
        collection_name = self._COLLECTION_MAPPING[resource_type]
        return getattr(self, collection_name)

    def get_association_by_resource(self, resource):
        """Get the association object from the corresponding collection by its resource id."""
        resource_type = self._get_resource_type(resource)
        collection = self._get_collection(resource_type)  # e.g., "expenses", "incomes"

        association = [
            association
            for association in collection
            if getattr(association, resource_type) == resource
        ]

        association = next(
            (
                assoc
                for assoc in collection
                if getattr(assoc, resource_type) == resource
            ),
            None,
        )

        if association is None:
            return None
        return association

    def _add_association(self, association):
        """Add the association object to the corresponding collection."""
        resource_type = self._get_resource_type(association)
        collection = self._get_collection(resource_type)  # e.g., "expenses", "incomes"

        if association in collection:
            raise ValueError(f"Association already exists in {collection.__name__}")
        collection.append(association)

    def _update_association(self, association, **param):
        """Update the association object from the corresponding collection by given parameters."""
        resource_type = self._get_resource_type(association)
        collection = self._get_collection(resource_type)  # e.g., "expenses", "incomes"

        return_association = next(
            (assoc for assoc in collection if assoc == association),
            None,
        )

        if return_association is None:
            raise ValueError(
                f"Association not found in the collection: {resource_type}"
            )

        for k, v in param.items():
            if hasattr(return_association, k):
                setattr(return_association, k, v)
            else:
                raise AttributeError(f"Association does not have attribute: {k}")

        return return_association

    def _delete_association(self, association):
        """Delete the association object from the corresponding collection"""
        resource_type = self._get_resource_type(association)
        collection = self._get_collection(resource_type)  # e.g., "expenses", "incomes"

        # Ensure the association is in the collection before removing
        if association not in collection:
            raise ValueError(
                f"Association {association} not found in the collection: {resource_type}"
            )

        collection.remove(association)

        return None
