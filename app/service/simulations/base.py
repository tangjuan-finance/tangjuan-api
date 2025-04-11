from typing import Type
from decimal import Decimal
from collections import defaultdict

from app.domain.simulations.strategies.utils import format_simulation_output
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
            raise ValueError("Missing required config: 'resource_type'")

        self.resource_type = resource_type
        self.start_attr = config.get("start_attr")
        self.end_attr = config.get("end_attr")
        self.default_strategy = config.get("default_strategy", "random_rate")
        self.valid_strategy = config.get("valid_strategy")
        self.strategy_param = config.get("strategy_param", {})
        self.domain_repo_class = config.get("domain_repo_class")

    def simulate_resource(self, account_id: str, payload: dict) -> dict:
        # Get the payload
        resource_id = self._get_resource_id_from_payload(self.resource_type, payload)
        strategy_name = payload.get("strategy", self.default_strategy)

        # Get asset
        resource = self._get_resource_domain_by_repo(
            resource_id=resource_id, repo=self.domain_repo_class
        )
        # Check if the account own the asset
        self._check_entity_ownership(account_id=account_id, entity=resource)

        # Get strategy
        strategy = self._build_strategy_from_resource(
            strategy_name=strategy_name, resource=resource
        )

        # Get start and end age
        start, end = (
            getattr(resource, self.start_attr),
            getattr(resource, self.end_attr),
        )

        return strategy.simulate_years(start=start, end=end, amount=resource.amount)

    def _get_resource_id_from_payload(self, resource_type: str, payload: dict) -> str:
        key = f"{self.resource_type}_id"
        resource_id = payload.get(key)
        if not resource_id:
            raise ValueError(f"Missing required field: '{key}'")
        return resource_id

    def _get_resource_domain_by_repo(
        self, resource_id: str, repo: ResourceRepo
    ) -> ResourceDomain:
        """
        Get the domain object of a resource using its repo and verify ownership.
        """
        resource = repo.get_by_id(resource_id)
        if not resource:
            raise ValueError(f"Resource with ID {resource_id} not found")
        return resource

    def _get_strategy_class(
        self, strategy: str, valid_strategies: dict
    ) -> Type[BaseSimulateStrategy]:
        """
        Get the strategy class from the list of valid strategies by its name.
        """
        strategy_class = valid_strategies.get(str(strategy))
        if not strategy_class:
            raise ValueError(f"Invalid strategy: '{strategy}'")

        return strategy_class

    def _build_strategy_from_resource(
        self, strategy_name: str, resource: ResourceDomain
    ):
        strategy_class = self._get_strategy_class(
            strategy=strategy_name, valid_strategies=self.valid_strategy
        )

        if strategy_class == RandomRateStrategy:
            # Get min-max attr
            min_attr = self.strategy_param.get("min_rate", "min_yearly_return_rate")
            max_attr = self.strategy_param.get("max_rate", "max_yearly_return_rate")

            # Get min-max value
            min_rate = getattr(resource, min_attr)
            if min_rate is None:
                raise ValueError("min rate should be given.")
            max_rate = getattr(resource, max_attr)
            if max_rate is None:
                raise ValueError("max rate should be given.")

            return RandomRateStrategy(min_rate=min_rate, max_rate=max_rate)

        raise ValueError(f"Unsupported strategy class: {strategy_class.__name__}")


class BaseAssociationSimulationService(BaseSimulationService):
    def __init__(self, config: dict):
        super().__init__(config)
        self.assoc_repo_class = config.get("assoc_repo_class")
        self.association_param = config.get("association_param", {})

    def simulate_resource_in_scenario(self, account_id: str, payload: dict) -> dict:
        # Validate account owns the scenario, scenario exist
        resource_id = self._get_resource_id_from_payload(self.resource_type, payload)
        strategy_name = payload.get("strategy", self.default_strategy)
        scenario_id = self._extract_scenario_id_from_payload(payload)
        self._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)

        # Get asset
        resource = self._get_resource_domain_by_repo(
            resource_id=resource_id, repo=self.domain_repo_class
        )
        # Check if the account own the asset
        self._check_entity_ownership(account_id=account_id, entity=resource)

        # Get assoc
        self._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        assoc = self._get_resource_association_by_repo(
            scenario_id=scenario_id,
            resource_id=resource_id,
            assoc_repo=self.assoc_repo_class,
        )

        return self._generate_simulation_by_resource_and_assoc(
            resource=resource, assoc=assoc, strategy_name=strategy_name
        )

    def simulate_resources_in_scenario(self, account_id: str, payload: dict) -> list:
        # Validate account owns the scenario, scenario exist
        strategy_name = payload.get("strategy", self.default_strategy)
        scenario_id = self._extract_scenario_id_from_payload(payload)
        self._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)

        # For assets belong to scenario
        assocs = self.assoc_repo_class.get_list(scenario_id)

        data = []
        for assoc in assocs:
            resource_id = getattr(assoc, f"{self.resource_type}_id")

            # Get asset
            resource = self._get_resource_domain_by_repo(
                resource_id=resource_id, repo=self.domain_repo_class
            )

            # Check if the account own the asset
            self._check_entity_ownership(account_id=account_id, entity=resource)

            # Run simulation
            simulation = self._generate_simulation_by_resource_and_assoc(
                resource=resource, assoc=assoc, strategy_name=strategy_name
            )
            data.append(
                {f"{self.resource_type}_id": resource_id, "simulation": simulation}
            )

        return data

    def aggregate_simulations_by_age(self, account_id: str, payload: dict) -> dict:
        simulations = self.simulate_resources_in_scenario(
            account_id=account_id, payload=payload
        )
        aggregate = defaultdict(Decimal)

        # Aggregate the value based on age
        for item in simulations:
            for age, value in zip(
                item["simulation"]["ages"], item["simulation"]["values"]
            ):
                aggregate[age] += value

        # Sort and formatted
        sorted_ages = sorted(aggregate.keys())
        return format_simulation_output(
            ages=sorted_ages, values=[aggregate[age] for age in sorted_ages]
        )

    def _generate_simulation_by_resource_and_assoc(
        self, resource: ResourceDomain, assoc: BaseAssociationDomain, strategy_name: str
    ) -> dict:
        strategy = self._build_strategy_from_resource_and_assoc(
            strategy_name=strategy_name, resource=resource, assoc=assoc
        )

        # Create start and end by asset and assoc
        start, end = self._get_years_from_resource_and_assoc(
            resource=resource,
            assoc=assoc,
            start_attr=self.start_attr,
            end_attr=self.end_attr,
        )

        return strategy.simulate_years(start=start, end=end, amount=resource.amount)

    def _extract_scenario_id_from_payload(self, payload) -> str:
        scenario_id = payload.get("scenario_id")
        if not scenario_id:
            raise ValueError("Missing required field: 'scenario_id'")

        return scenario_id

    def _check_scenario_ownership(self, account_id: str, scenario_id: str) -> None:
        """
        Check if the account own this scenario
        """

        # Get scenario by ID
        scenario = ScenarioRepo.get_by_id(scenario_id)
        if not scenario:
            raise ValueError(f"Scenario with ID {scenario_id} not found")

        # Check if the account own the scenario
        self._check_entity_ownership_by_id(
            account_id=account_id, owner_id=scenario.owner.id
        )
        return None

    def _get_resource_association_by_repo(
        self,
        scenario_id: str,
        resource_id: str,
        assoc_repo: AssociationRepo,
    ) -> BaseAssociationDomain:
        """
        Get the association of a resource using its repo and verify ownership.
        """
        assoc = assoc_repo.get_by_id(scenario_id, resource_id)
        if not assoc:
            raise ValueError(
                f"Resource with ID {resource_id} not in scenario {scenario_id}."
            )

        return assoc

    def _get_years_from_resource_and_assoc(
        self,
        resource: ResourceDomain,
        assoc: BaseAssociationDomain,
        start_attr: str,
        end_attr: str,
    ) -> tuple:
        start = getattr(assoc, start_attr) or getattr(resource, start_attr)
        end = getattr(assoc, end_attr) or getattr(resource, end_attr)
        return start, end

    def _build_strategy_from_resource_and_assoc(
        self, strategy_name: str, resource: ResourceDomain, assoc: BaseAssociationDomain
    ):
        strategy_class = self._get_strategy_class(
            strategy=strategy_name, valid_strategies=self.valid_strategy
        )

        if strategy_class == RandomRateStrategy:
            # Get min-max attr
            min_attr = self.strategy_param.get("min_rate", "min_yearly_return_rate")
            max_attr = self.strategy_param.get("max_rate", "max_yearly_return_rate")

            # Get min-max value from assoc or resource
            min_rate = getattr(assoc, min_attr) or getattr(resource, min_attr)
            if min_rate is None:
                raise ValueError("min rate should be given.")
            max_rate = getattr(assoc, max_attr) or getattr(resource, max_attr)
            if max_rate is None:
                raise ValueError("max rate should be given.")

            return RandomRateStrategy(min_rate=min_rate, max_rate=max_rate)

        raise ValueError(f"Unsupported strategy class: {strategy_class.__name__}")
