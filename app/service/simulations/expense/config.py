from app.domain.simulations.strategies import RandomRateStrategy
from app.repository.entities import ExpenseRepo
from app.repository.associations import ScenarioExpenseRepo
from types import MappingProxyType

# Create immutable dict for config
ExpenseSimulationConfig = MappingProxyType(
    {
        "resource_type": "expense",
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
        "domain_repo_class": ExpenseRepo,
    }
)

ScenarioExpenseSimulationConfig = MappingProxyType(
    {
        **ExpenseSimulationConfig,
        "assoc_repo_class": ScenarioExpenseRepo,
    }
)
