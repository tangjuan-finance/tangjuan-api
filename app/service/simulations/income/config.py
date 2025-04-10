from app.domain.simulations.strategies import RandomRateStrategy
from app.repository.entities import IncomeRepo
from app.repository.associations import ScenarioIncomeRepo
from types import MappingProxyType

# Create immutable dict for config
IncomeSimulationConfig = MappingProxyType(
    {
        "resource_type": "income",
        "start_attr": "start_age",
        "end_attr": "end_age",
        "default_strategy": "random_rate",
        "valid_strategy": {
            "random_rate": RandomRateStrategy,
        },
        "strategy_param": {
            "min_rate": "min_yearly_growth_rate",
            "max_rate": "max_yearly_growth_rate",
        },
        "domain_repo_class": IncomeRepo,
    }
)

ScenarioIncomeSimulationConfig = MappingProxyType(
    {
        **IncomeSimulationConfig,
        "assoc_repo_class": ScenarioIncomeRepo,
    }
)
