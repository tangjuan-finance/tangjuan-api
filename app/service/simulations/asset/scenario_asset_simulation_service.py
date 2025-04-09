from app.service.simulations.base import BaseAssociationSimulationService
from app.domain.simulations.strategies import RandomRateStrategy
from app.domain.entities import AssetDomain
from app.domain.associations import ScenarioAssetDomain
from .base import BaseAssetSimulation

from app.repository.entities import AssetRepo
from app.repository.associations import ScenarioAssetRepo
from decimal import Decimal
from collections import defaultdict


class ScenarioAssetSimulationService(
    BaseAssociationSimulationService, BaseAssetSimulation
):
    @classmethod
    def simulate_asset_in_scenario(cls, account_id: str, payload: dict) -> dict:
        # Validate input
        asset_id, scenario_id, strategy_name = cls.validate_assoc_simulation_input(
            payload=payload,
            resource_type="asset",
            default_strategy=cls.DEFAULT_STRATEGY,
        )

        # Get asset
        asset = cls._get_resource_domain_by_repo(
            account_id=account_id, entity_id=asset_id, repo=AssetRepo
        )

        # Get assoc
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)
        assoc = cls._get_resource_association_by_repo(
            scenario_id=scenario_id,
            entity_id=asset_id,
            assoc_repo=ScenarioAssetRepo,
        )

        # Generate simulation
        return cls._generate_simulation_by_asset_and_assoc(
            asset=asset, assoc=assoc, strategy_name=strategy_name
        )

    @classmethod
    def simulate_assets_in_scenario(cls, account_id: str, payload: dict) -> dict:
        # Validate account own the scenario, scenario exist
        strategy_name = cls.get_strategy_name_from_payload(
            payload=payload, default_strategy=cls.DEFAULT_STRATEGY
        )
        scenario_id = cls.get_scenario_id_from_payload(payload)
        cls._check_scenario_ownership(account_id=account_id, scenario_id=scenario_id)

        # For assets belong to scenario
        assocs = ScenarioAssetRepo.get_list(scenario_id)
        data = []
        for assoc in assocs:
            # Get asset
            asset = cls._get_resource_domain_by_repo(
                account_id=account_id, entity_id=assoc.asset_id, repo=AssetRepo
            )

            # Run simulation
            simulation = cls._generate_simulation_by_asset_and_assoc(
                asset=asset, assoc=assoc, strategy_name=strategy_name
            )
            data.append({"asset_id": asset.id, "simulation": simulation})

        return data

    @classmethod
    def aggregate_assets_in_scenario(cls, account_id: str, payload: dict) -> dict:
        data = cls.simulate_assets_in_scenario(account_id=account_id, payload=payload)
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

    @classmethod
    def _generate_simulation_by_asset_and_assoc(
        cls, asset: AssetDomain, assoc: ScenarioAssetDomain, strategy_name: str
    ) -> dict:
        # Get strategy
        strategy = cls._build_strategy_from_asset_and_assoc(
            strategy_name=strategy_name, asset=asset, assoc=assoc
        )

        # Create start and end by asset and assoc
        start = getattr(assoc, "start_age") or asset.start_age
        end = getattr(assoc, "end_age") or asset.end_age

        return cls._generate_simulation(
            amount=asset.amount,
            start=start,
            end=end,
            strategy=strategy,
        )

    @classmethod
    def _build_strategy_from_asset_and_assoc(
        cls, strategy_name: str, asset: AssetDomain, assoc: ScenarioAssetDomain
    ):
        strategy_class = cls._get_strategy_class(
            strategy=strategy_name, valid_strategies=cls.VALID_STRATEGY
        )

        if strategy_class == RandomRateStrategy:
            min_rate = getattr(assoc, "min_yearly_return_rate") or getattr(
                asset, "min_yearly_return_rate"
            )
            if min_rate is None:
                raise ValueError("min rate should be given.")
            max_rate = getattr(assoc, "max_yearly_return_rate") or getattr(
                asset, "max_yearly_return_rate"
            )
            if max_rate is None:
                raise ValueError("max rate should be given.")

            return RandomRateStrategy(min_rate=min_rate, max_rate=max_rate)

        raise ValueError(f"Unsupported strategy class: {strategy_class.__name__}")
