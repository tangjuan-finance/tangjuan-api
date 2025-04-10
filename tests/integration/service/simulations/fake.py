from decimal import Decimal

from app.service.simulations.base import BaseSimulationService
from app.domain.simulations.strategies import BaseSimulateStrategy


class FakeSimulationService(BaseSimulationService):
    def _fake_entity_simulate(
        self,
        amount: Decimal,
        start_age: int,
        end_age: int,
        strategy: BaseSimulateStrategy,
    ) -> dict:
        return self._format_output(
            ages=self._get_duration(start=start_age, end=end_age),
            values=self._simulate(
                amount=amount,
                start=start_age,
                end=end_age,
                strategy=strategy,
            ),
        )
