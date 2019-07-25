"""
"""

from abc import ABC, abstractmethod
from typing import Iterable

from core.database import Database
from core.function import Function, FunctionSample
from core.source import Source


class Instantiator(ABC):
    """
    """

    def __init__(self, database: Database):
        self._database: Database = database

    @abstractmethod
    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        pass
