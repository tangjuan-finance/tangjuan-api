from types import MappingProxyType

resources_type_map = MappingProxyType(
    {
        "ExpenseDomain": {"name": "expense", "names": "expenses"},
        "IncomeDomain": {"name": "income", "names": "incomes"},
        "HouseDomain": {"name": "house", "names": "houses"},
        "ChildDomain": {"name": "child", "names": "children"},
        "RiskDomain": {"name": "risk", "names": "risks"},
        "AssetDomain": {"name": "asset", "names": "assets"},
        "LiabilityDomain": {"name": "liability", "names": "liabilities"},
    }
)
