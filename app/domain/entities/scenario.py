from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from .base import EntityDomain

if TYPE_CHECKING:
    from .account import AccountDomain
    from ..associations import (
        ScenarioExpenseDomain,
        ScenarioIncomeDomain,
        ScenarioHouseDomain,
        ScenarioChildDomain,
        ScenarioRiskDomain,
        ScenarioAssetDomain,
        ScenarioLiabilityDomain,
    )
    from app.mapper.resource_mapper import ResourceMapper


@dataclass(kw_only=True)
class ScenarioDomain(EntityDomain):
    owner: "AccountDomain"
    name: str
    asset_allocation_percentage: Decimal
    retire_age: int
    description: Optional[str] = None

    # Resource collections
    expenses: List["ScenarioExpenseDomain"] = field(default_factory=list)
    incomes: List["ScenarioIncomeDomain"] = field(default_factory=list)
    houses: List["ScenarioHouseDomain"] = field(default_factory=list)
    children: List["ScenarioChildDomain"] = field(default_factory=list)
    risks: List["ScenarioRiskDomain"] = field(default_factory=list)
    assets: List["ScenarioAssetDomain"] = field(default_factory=list)
    liabilities: List["ScenarioLiabilityDomain"] = field(default_factory=list)

    def _get_collection(self, mapper: "ResourceMapper"):
        """Get collection by mapping a resource type to its corresponding collection name."""
        return getattr(self, mapper.collection_type)

    def get_association_by_resource(self, resource):
        """Get the association object from the corresponding collection by its resource id."""
        from app.mapper.resource_mapper import ResourceMapper

        resource_mapper = ResourceMapper.from_domain(resource)
        resource_type = resource_mapper.resource_type
        collection = self._get_collection(
            resource_mapper
        )  # e.g., "expenses", "incomes"

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
        from app.mapper.resource_mapper import ResourceMapper

        resource_mapper = ResourceMapper.from_assoc(association)
        collection = self._get_collection(
            resource_mapper
        )  # e.g., "expenses", "incomes"

        if association in collection:
            raise ValueError(f"Association already exists in {collection.__name__}")
        collection.append(association)

    def _update_association(self, association, **param):
        """Update an existing association in the collection with given parameters."""
        from app.mapper.resource_mapper import ResourceMapper

        # Map the association to its resource type (e.g., Expense, Income)
        resource_mapper = ResourceMapper.from_assoc(association)
        resource_type = resource_mapper.resource_type  # e.g., "expense", "income"

        # Retrieve the corresponding collection from Scenario (e.g., expenses, incomes)
        collection = self._get_collection(
            resource_mapper
        )  # e.g., "expenses", "incomes"

        # Find the matching association by comparing assoc's resource
        return_association = next(
            (
                assoc
                for assoc in collection
                if getattr(assoc, resource_type) == getattr(association, resource_type)
            ),
            None,
        )

        if return_association is None:
            raise ValueError(
                f"Association not found in the collection: {resource_type}"
            )

        # Update attributes safely
        for k, v in param.items():
            if hasattr(return_association, k):
                setattr(return_association, k, v)
            else:
                raise AttributeError(f"Association does not have attribute: {k}")

        return return_association

    def _delete_association(self, association):
        """Delete the association object from the corresponding collection"""
        from app.mapper.resource_mapper import ResourceMapper

        resource_mapper = ResourceMapper.from_assoc(association)
        resource_type = resource_mapper.resource_type
        collection = self._get_collection(
            resource_mapper
        )  # e.g., "expenses", "incomes"

        # Ensure the association is in the collection before removing
        if association not in collection:
            raise ValueError(
                f"Association {association} not found in the collection: {resource_type}"
            )

        collection.remove(association)

        return None
