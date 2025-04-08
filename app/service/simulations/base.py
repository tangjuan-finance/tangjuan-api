from typing import Type
from decimal import Decimal, ROUND_UP

from app.domain.simulations.strategies import BaseSimulateStrategy
from app.repository.entities import ResourceRepo
from app.domain.entities import ResourceDomain
from app.service.mixin import CheckOwnershipMixin
from app.repository.entities import ScenarioRepo
from app.repository.associations import AssociationRepo
from app.domain.associations import BaseAssociationDomain


class BaseSimulationService(CheckOwnershipMixin):
    @classmethod
    def validate_simulation_input(
        cls, payload: dict, resource_type: str, default_strategy: str
    ) -> tuple[str, str]:
        """Validates and returns (resource_id, strategy_name)"""
        resource_id_key = f"{resource_type}_id"
        resource_id = payload.get(resource_id_key)
        strategy_name = payload.get("strategy", default_strategy)

        missing = []
        if not resource_id:
            missing.append(resource_id_key)

        if missing:
            raise ValueError(f"Missing required field(s): {', '.join(missing)}")

        return resource_id, strategy_name

    @classmethod
    def _get_resource_domain_by_repo(
        cls, account_id: str, entity_id: str, repo: ResourceRepo
    ) -> ResourceDomain:
        """
        Get the domain object of a resource using its repo and verify ownership.
        """
        entity = repo.get_by_id(entity_id)
        if not entity:
            raise ValueError(f"Resource with ID {entity_id} not found")

        # Get owner ID from either parent or directly
        owner_id = (
            getattr(entity.parent, "id", None)
            if hasattr(entity, "parent")
            else entity.owner.id
        )

        # Check if the account own the resource
        cls._check_ownership_by_id(account_id=account_id, owner_id=owner_id)
        return entity

    @classmethod
    def _get_strategy_class(
        cls, strategy: str, valid_strategies: dict
    ) -> Type[BaseSimulateStrategy]:
        """
        Get the strategy class from the list of valid strategies by its name.
        """
        strategy_class = valid_strategies.get(str(strategy))
        if not strategy_class:
            raise ValueError(f"Invalid strategy {strategy}")

        return strategy_class

    @classmethod
    def _generate_simulation(
        cls, amount: int, start: int, end: int, strategy: BaseSimulateStrategy
    ):
        """
        Generate simulated values and corresponding ages over a range.
        """
        ages = cls._get_duration(start=start, end=end)
        values = cls._simulate(
            amount=amount,
            start=start,
            end=end,
            strategy=strategy,
        )
        return {
            "ages": ages,
            "values": values,
        }

    @classmethod
    def _get_duration(cls, start: int, end: int) -> list:
        """
        Generate a list of years from start to end (inclusive).
        """
        return list(range(start, end + 1))

    @classmethod
    def _simulate(
        cls, amount: int, start: int, end: int, strategy: BaseSimulateStrategy
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


class BaseAssociationSimulationService(BaseSimulationService):
    @classmethod
    def validate_assoc_simulation_input(
        cls, payload: dict, resource_type: str, default_strategy: str
    ) -> tuple[str, str, str]:
        """Validates and returns (resource_id, scenario_id, strategy_name)"""

        # Validate the simulation inputs first
        resource_id, strategy_name = cls.validate_simulation_input(
            payload=payload,
            resource_type=resource_type,
            default_strategy=default_strategy,
        )

        # Validate scenario id
        scenario_id = payload.get("scenario_id")
        if not scenario_id:
            raise ValueError(f"Missing required field: {scenario_id}")

        return resource_id, scenario_id, strategy_name

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
        cls._check_ownership_by_id(account_id=account_id, owner_id=scenario.owner.id)
        return None

    @classmethod
    def _get_resource_association_by_repo(
        cls,
        account_id: str,
        scenario_id: str,
        entity_id: str,
        assoc_repo: AssociationRepo,
    ) -> BaseAssociationDomain:
        """
        Get the association of a resource using its repo and verify ownership.
        """
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        assoc = assoc_repo.get_by_id(scenario_id, entity_id)
        if not assoc:
            raise ValueError(
                f"Resource with ID {entity_id} not in scenario {scenario_id}."
            )

        return assoc
