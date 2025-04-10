from app.domain.simulations.strategies import RandomRateStrategy
from app.repository.entities import AssetRepo
from types import MappingProxyType

# Create immutable dict for config
AssetSimulationConfig = MappingProxyType(
    {
        "resource_type": "asset",
        "default_strategy": "random_rate",
        "valid_strategy": {
            "random_rate": RandomRateStrategy,
        },
        "strategy_param": {
            "min_rate": "min_yearly_return_rate",
            "max_rate": "max_yearly_return_rate",
        },
        "domain_repo_class": AssetRepo,
    }
)

# class AssetSimulationMixin:
#     RESOURCE_TYPE = "asset"
#     VALID_STRATEGY = {
#         "random_rate": RandomRateStrategy,
#     }
#     STRATEGY_PARAM = {
#         "min_rate": "min_yearly_return_rate",
#         "max_rate": "max_yearly_return_rate",
#     }
#     DEFAULT_STRATEGY = "random_rate"
