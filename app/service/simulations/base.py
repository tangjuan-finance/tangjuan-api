from abc import ABC
from app.service.mixin import CheckOwnershipMixin


class BaseSimulationService(ABC, CheckOwnershipMixin):
    pass
