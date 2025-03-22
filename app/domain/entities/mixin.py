from dataclasses import dataclass
from typing import Optional


# For resources which need an age range
@dataclass(kw_only=True)
class BaseAgeIntervalMixin:
    start_age: int
    end_age: Optional[int] = None
