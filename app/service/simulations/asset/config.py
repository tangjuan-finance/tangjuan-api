from app.domain.simulations.strategies import RandomRateStrategy
from app.repository.entities import AssetRepo
from app.repository.associations import ScenarioAssetRepo
from types import MappingProxyType

# Create immutable dict for config
AssetSimulationConfig = MappingProxyType(
    {
        "resource_type": "asset",
        "start_attr": "start_age",
        "end_attr": "end_age",
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

ScenarioAssetSimulationConfig = MappingProxyType(
    {
        **AssetSimulationConfig,
        "assoc_repo_class": ScenarioAssetRepo,
    }
)
