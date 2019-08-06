"""
This module contains the definition of the DefaultSampler.
"""

import logging
from typing import Iterable

from core.sampler import Sampler
from core.database import Database
from core.variable import Variable
from core.function import Function
from core.sample import FunctionSample


class ValidSingleSampler(Sampler):
    """
    """

    def __init__(self, database: Database) -> None:
        super().__init__(database)

    def __str__(self) -> str:
        return type(self).__name__

    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        """
        """


