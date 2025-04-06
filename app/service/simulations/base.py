from abc import ABC
from typing import Type
from decimal import Decimal, ROUND_UP

from app.domain.simulations.strategies import BaseSimulateStrategy
from app.repository.entities import ResourceRepo
from app.domain.entities import ResourceDomain
from app.service.mixin import CheckOwnershipMixin


class BaseSimulationService(ABC, CheckOwnershipMixin):
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

        # Check if the account own the asset
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


class GetAssociationDomainMixin:
    @classmethod
    def _get_resource_association_by_repo(
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

        # Check if the account own the asset
        cls._check_ownership_by_id(account_id=account_id, owner_id=owner_id)
        return entity
