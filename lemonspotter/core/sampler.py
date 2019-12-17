"""
"""

from abc import ABC, abstractmethod
from typing import Iterable
import logging

from lemonspotter.core.database import Database
from lemonspotter.core.function import Function
from lemonspotter.core.sample import FunctionSample


class Sampler(ABC):
    """
    """

    @abstractmethod
    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        """
        Generate FunctionSample objects from a given function according to an
        individual Samplers specification.
        """

        return set()

    @classmethod
    def _generate_empty_sample(cls, function: Function) -> Iterable[FunctionSample]:
        """
        Generate a FunctionSample for functions which don't have any parameters.
        """

        logging.debug('%s has no arguments.', function.name)

        sample = FunctionSample(function, True)

        def evaluator(sample=sample) -> bool:
            return (sample.return_variable.value ==
                    Database().get_constant('MPI_SUCCESS').value)

        sample.evaluator = evaluator

        return {sample}
