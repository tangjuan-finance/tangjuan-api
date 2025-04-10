from typing import Type
from decimal import Decimal, ROUND_UP
from collections import defaultdict

from app.domain.simulations.strategies import BaseSimulateStrategy, RandomRateStrategy
from app.repository.entities import ResourceRepo
from app.domain.entities import ResourceDomain
from app.service.mixin import CheckOwnershipMixin
from app.repository.entities import ScenarioRepo
from app.repository.associations import AssociationRepo
from app.domain.associations import BaseAssociationDomain


class BaseSimulationService(CheckOwnershipMixin):
    def __init__(self, config: dict):
        # Get the config
        resource_type = config.get("resource_type")
        if not resource_type:
            raise ValueError("Resource type is required")

        self.resource_type = resource_type
        self.default_strategy = config.get("default_strategy", "random_rate")
        self.valid_strategy = config.get("valid_strategy")
        self.strategy_param = config.get("strategy_param")
        self.domain_repo_class = config.get("domain_repo_class")

    def simulate_entity(self, account_id: str, payload: dict) -> dict:
        # Get the payload
        entity_id = self._get_resource_id_from_payload(self.resource_type, payload)
        strategy_name = payload.get("strategy", self.default_strategy)

        # Get asset
        entity = self._get_resource_domain_by_repo(
            entity_id=entity_id, repo=self.domain_repo_class
        )
        # Check if the account own the asset
        self._check_entity_ownership(account_id=account_id, entity=entity)

        # Get strategy
        strategy = self._build_strategy_from_entity(
            strategy_name=strategy_name, entity=entity
        )

        # Get start and end age
        start, end = entity.start_age, entity.end_age

        return self._format_output(
            ages=self._get_duration(start=start, end=end),
            values=self._simulate(
                amount=entity.amount,
                start=start,
                end=end,
                strategy=strategy,
            ),
        )

    def validate_simulation_input(
        self, payload: dict, resource_type: str, default_strategy: str
    ) -> tuple[str, str]:
        """Validates and returns (resource_id, strategy_name)"""
        resource_id = self._get_resource_id_from_payload(resource_type, payload)
        strategy_name = self.extract_strategy_name_from_payload(
            payload, default_strategy
        )

        return resource_id, strategy_name

    def _get_resource_id_from_payload(self, resource_type: str, payload: dict) -> str:
        resource_id_key = f"{resource_type}_id"
        resource_id = payload.get(resource_id_key)

        if not resource_id:
            raise ValueError(f"Missing {resource_type}")

        return resource_id

    # def extract_strategy_name_from_payload(
    #     self, payload: dict, default_strategy: str
    # ) -> str:
    #     return payload.get("strategy", default_strategy)

    def _get_resource_domain_by_repo(
        self, entity_id: str, repo: ResourceRepo
    ) -> ResourceDomain:
        """
        Get the domain object of a resource using its repo and verify ownership.
        """
        entity = repo.get_by_id(entity_id)
        if not entity:
            raise ValueError(f"Resource with ID {entity_id} not found")
        return entity

    def _get_strategy_class(
        self, strategy: str, valid_strategies: dict
    ) -> Type[BaseSimulateStrategy]:
        """
        Get the strategy class from the list of valid strategies by its name.
        """
        strategy_class = valid_strategies.get(str(strategy))
        if not strategy_class:
            raise ValueError(f"Invalid strategy {strategy}")

        return strategy_class

    def _build_strategy_from_entity(self, strategy_name: str, entity: ResourceDomain):
        strategy_class = self._get_strategy_class(
            strategy=strategy_name, valid_strategies=self.valid_strategy
        )

        if strategy_class == RandomRateStrategy:
            # Get min-max attr
            min_attr = self.strategy_param.get("min_rate", "min_yearly_return_rate")
            max_attr = self.strategy_param.get("max_rate", "max_yearly_return_rate")

            # Get min-max value
            min_rate = getattr(entity, min_attr)
            if min_rate is None:
                raise ValueError("min rate should be given.")
            max_rate = getattr(entity, max_attr)
            if max_rate is None:
                raise ValueError("max rate should be given.")

            return RandomRateStrategy(min_rate=min_rate, max_rate=max_rate)

        raise ValueError(f"Unsupported strategy class: {strategy_class.__name__}")

    # @classmethod
    # def _generate_simulation(
    #     cls, amount: int, start: int, end: int, strategy: BaseSimulateStrategy
    # ):
    #     """
    #     Generate simulated values and corresponding ages over a range.
    #     """
    #     return cls._format_output(
    #         ages=cls._get_duration(start=start, end=end),
    #         values=cls._simulate(
    #             amount=amount,
    #             start=start,
    #             end=end,
    #             strategy=strategy,
    #         ),
    #     )

    def _get_duration(self, start: int, end: int) -> list:
        """
        Generate a list of years from start to end (inclusive).
        """
        return list(range(start, end + 1))

    def _simulate(
        self, amount: int, start: int, end: int, strategy: BaseSimulateStrategy
    ) -> list:
        """
        Simulate value growth over a given period using a simulation strategy.
        """
        prev = Decimal(amount).quantize(exp=Decimal("1.00"), rounding=ROUND_UP)
        values = [prev]

        for _ in range(start + 1, end + 1):
            prev = strategy.apply(prev)
            values.append(prev)
        return values

    def _format_output(self, ages: list, values: list) -> dict:
        """
        Format output
        """
        return {
            "ages": ages,
            "values": values,
        }


class BaseAssociationSimulationService(BaseSimulationService):
    @classmethod
    def extract_scenario_id_from_payload(cls, payload) -> str:
        scenario_id = payload.get("scenario_id")
        if not scenario_id:
            raise ValueError(f"Missing required field: {scenario_id}")

        return scenario_id

    @classmethod
    def _check_scenario_ownership(cls, account_id: str, scenario_id: str) -> None:
        """
        Check if the account own this scenario
        """

        # Get scenario by ID
        scenario = ScenarioRepo.get_by_id(scenario_id)
        if not scenario:
            raise ValueError(f"Scenario with ID {scenario_id} not found")

        # Check if the account own the scenario
        cls._check_entity_ownership_by_id(
            account_id=account_id, owner_id=scenario.owner.id
        )
        return None

    @classmethod
    def _get_resource_association_by_repo(
        cls,
        scenario_id: str,
        entity_id: str,
        assoc_repo: AssociationRepo,
    ) -> BaseAssociationDomain:
        """
        Get the association of a resource using its repo and verify ownership.
        """
        assoc = assoc_repo.get_by_id(scenario_id, entity_id)
        if not assoc:
            raise ValueError(
                f"Resource with ID {entity_id} not in scenario {scenario_id}."
            )

        return assoc

    @classmethod
    def _get_years_from_entity_and_assoc(
        cls,
        entity: ResourceDomain,
        assoc: BaseAssociationDomain,
        start_attr: str,
        end_attr: str,
    ) -> tuple:
        start = getattr(assoc, start_attr) or getattr(entity, start_attr)
        end = getattr(assoc, end_attr) or getattr(entity, end_attr)
        return start, end

    @classmethod
    def _aggregate_simulations_by_age(cls, data: dict) -> dict:
        aggregate = defaultdict(Decimal)

        # Aggregate the value based on age
        for item in data:
            sim = item["simulation"]
            for age, value in zip(sim["ages"], sim["values"]):
                aggregate[age] += value

        # Sort and formatted
        sorted_ages = sorted(aggregate.keys())
        return cls._format_output(
            ages=sorted_ages, values=[aggregate[age] for age in sorted_ages]
        )
