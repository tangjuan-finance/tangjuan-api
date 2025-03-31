from app.mapper.resource_mapper import ResourceMapper
from types import MappingProxyType
from tests.unit.factories import (
    ExpenseDomainFactory,
    IncomeDomainFactory,
    HouseDomainFactory,
    ChildDomainFactory,
    RiskDomainFactory,
    AssetDomainFactory,
    LiabilityDomainFactory,
)


class ResourceTestMapper(ResourceMapper):
    _RESOURCE_DOMAIN_FACTORY_MAPPING = MappingProxyType(
        {
            "child": ChildDomainFactory,
            "liability": LiabilityDomainFactory,
            "expense": ExpenseDomainFactory,
            "income": IncomeDomainFactory,
            "house": HouseDomainFactory,
            "risk": RiskDomainFactory,
            "asset": AssetDomainFactory,
        }
    )

    @property
    def resource_domain_factory(self):
        return self._RESOURCE_DOMAIN_FACTORY_MAPPING[self._resource_type]
