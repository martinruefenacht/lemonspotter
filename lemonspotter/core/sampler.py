"""
"""

from abc import ABC, abstractmethod
from typing import Iterable

from core.database import Database
from core.function import Function
from core.sample import FunctionSample


class Sampler(ABC):
    """
    """

    def __init__(self, database: Database):
        self._db: Database = database

    @abstractmethod
    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        return []
