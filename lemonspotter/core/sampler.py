"""
"""

from abc import ABC, abstractmethod
from typing import Iterable

from core.function import Function
from core.sample import FunctionSample


class Sampler(ABC):
    """
    """

    @abstractmethod
    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        return []
