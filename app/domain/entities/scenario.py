from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from .base import EntityDomain
from ..associations import BaseAssociationDomain


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
        BaseAssociationDomain,
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

    def _get_resource_id(
        self, association: "BaseAssociationDomain", resource_type: str
    ):
        return getattr(association, f"{resource_type}_id")

    def get_association_by_resource_id(
        self, resource_type: str, resource_id: str
    ) -> "BaseAssociationDomain":
        """Get the association object from the corresponding collection by its resource id."""
        from app.mapper.resource_mapper import ResourceMapper

        resource_mapper = ResourceMapper.by_resource_type(resource_type)
        collection = self._get_collection(
            resource_mapper
        )  # e.g., "expenses", "incomes"

        match_associations = [
            assoc
            for assoc in collection
            if getattr(assoc, f"{resource_type}_id") == resource_id
        ]

        if not match_associations:
            return None

        if len(match_associations) > 1:
            raise ValueError(
                f"Duplicate {resource_type.capitalize} Association: {match_associations}"
            )

        return match_associations[0]

    def _check_association_existed(
        self,
        association: "BaseAssociationDomain",
        resource_type: str,
        collection: List["BaseAssociationDomain"],
    ) -> str:
        """Check if given association existed in this scenario"""

        assoc_resource_id = self._get_resource_id(
            association=association, resource_type=resource_type
        )
        match_associations = [
            assoc
            for assoc in collection
            if getattr(assoc, f"{resource_type}_id") == assoc_resource_id
        ]

        if len(match_associations) != 0:
            raise ValueError(
                f"Association with resource ID {assoc_resource_id} already exists in {resource_type} collection"
            )

        return f"Association with resource ID {assoc_resource_id} is not in {resource_type} collection"

    def _check_assoc_validity(self, association: "BaseAssociationDomain") -> str:
        # Check if given associatio is an AssociationDomain
        if not isinstance(association, BaseAssociationDomain):
            raise TypeError(f"Given object {association} is not association")

        # Check is the scenario of given assoc is the same as this scenario
        if association.scenario_id != self.id:
            raise ValueError("Given association is not belong to this scenario")

        return (
            "Given association is an AssociationDomain object belong to this scenario"
        )

    def _add_association(self, association):
        """Add the association object to the corresponding collection."""
        self._check_assoc_validity(association)

        from app.mapper.resource_mapper import ResourceMapper

        resource_mapper = ResourceMapper.from_assoc(association)
        resource_type = resource_mapper.resource_type
        collection = self._get_collection(
            resource_mapper
        )  # e.g., "expenses", "incomes"

        self._check_association_existed(
            association=association, resource_type=resource_type, collection=collection
        )

        collection.append(association)

    def _update_association(self, association, **param):
        """Update an existing association in the collection with given parameters."""
        self._check_assoc_validity(association)

        from app.mapper.resource_mapper import ResourceMapper

        # Map the association to its resource type (e.g., Expense, Income)
        resource_mapper = ResourceMapper.from_assoc(association)
        resource_type = resource_mapper.resource_type  # e.g., "expense", "income"

        # Get the Resource ID
        resource_id = self._get_resource_id(
            association=association, resource_type=resource_type
        )

        # Get the association in given scenario
        return_association = self.get_association_by_resource_id(
            resource_type=resource_type, resource_id=resource_id
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
        self._check_assoc_validity(association)

        from app.mapper.resource_mapper import ResourceMapper

        # Map the association to its resource type (e.g., Expense, Income)
        resource_mapper = ResourceMapper.from_assoc(association)
        resource_type = resource_mapper.resource_type  # e.g., "expense", "income"

        # Get the Resource ID
        resource_id = self._get_resource_id(
            association=association, resource_type=resource_type
        )

        # Get the association in given scenario
        return_association = self.get_association_by_resource_id(
            resource_type=resource_type, resource_id=resource_id
        )

        if return_association is None:
            raise ValueError(
                f"Association not found in the collection: {resource_type}"
            )

        collection = self._get_collection(
            resource_mapper
        )  # e.g., "expenses", "incomes"

        collection.remove(association)

        return None
