from app.domain.simulations.strategies import RandomRateStrategy


class BaseAssetSimulation:
    VALID_STRATEGY = {
        "random_rate": RandomRateStrategy,
    }
    DEFAULT_STRATEGY = "random_rate"
