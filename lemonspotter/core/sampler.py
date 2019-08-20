"""
"""

from abc import ABC, abstractmethod
from typing import Iterable

from lemonspotter.core.function import Function
from lemonspotter.core.sample import FunctionSample


class Sampler(ABC):
    """
    """

    @abstractmethod
    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        return []
