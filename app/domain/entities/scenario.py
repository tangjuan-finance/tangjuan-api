from dataclasses import dataclass, field
from typing import Optional, List
from decimal import Decimal
from .base import EntityDomain
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

from .mapper import resources_type_map

# Mapping of class names to actual classes
scenario_association_classes = {
    "expense": ScenarioExpenseDomain,
    "income": ScenarioIncomeDomain,
    "house": ScenarioHouseDomain,
    "child": ScenarioChildDomain,
    "risk": ScenarioRiskDomain,
    "asset": ScenarioAssetDomain,
    "liability": ScenarioLiabilityDomain,
}


@dataclass(kw_only=True)
class ScenarioDomain(EntityDomain):
    owner: AccountDomain
    name: str
    asset_allocation_percentage: Decimal
    retire_age: int
    description: Optional[str] = None

    # Resource collections
    expenses: List[ScenarioExpenseDomain] = field(default_factory=list)
    incomes: List[ScenarioIncomeDomain] = field(default_factory=list)
    houses: List[ScenarioHouseDomain] = field(default_factory=list)
    children: List[ScenarioChildDomain] = field(default_factory=list)
    risks: List[ScenarioRiskDomain] = field(default_factory=list)
    assets: List[ScenarioAssetDomain] = field(default_factory=list)
    liabilities: List[ScenarioLiabilityDomain] = field(default_factory=list)

    def add_resource(self, resource_instance, **resource_data):
        """Adding a resource instance to the corresponding collections."""
        resource_cls = type(resource_instance).__name__
        if resource_cls not in resources_type_map:
            KeyError(f"Invalid resource class: {resource_cls}")
        else:
            resource_type = resources_type_map[resource_cls]

        cls_obj = scenario_association_classes[resource_type["name"]]
        association = cls_obj(
            scenario=self,
            **{
                resource_type["name"]: resource_instance
            },  # Dynamically set the right parameter
            **resource_data,
        )

        # Append to the correct collection
        collection = getattr(self, resource_type["name"])
        collection.append(association)

        return association
