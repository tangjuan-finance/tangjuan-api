from abc import ABC
from app.service.mixin import CheckOwnershipMixin


class BaseSimulationService(ABC, CheckOwnershipMixin):
    @classmethod
    def _get_duration(cls, start: int, end: int) -> list:
        return list(range(start, end + 1))
