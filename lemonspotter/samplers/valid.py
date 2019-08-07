"""
This module contains the definition of the DefaultSampler.
"""

import logging
from typing import Iterable, Sequence
import itertools

from core.sampler import Sampler
from core.database import Database
from core.variable import Variable
from core.function import Function
from core.sample import FunctionSample
from core.parameter import Parameter


class ValidSampler(Sampler):
    """
    """

    def __init__(self, database: Database) -> None:
        super().__init__(database)

    def __str__(self) -> str:
        return type(self).__name__

    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        """
        """

        argument_lists: Iterable[Iterable[Variable]] = []

        for parameter in function.parameters:
            argument_lists.append(self.generate_sample(parameter))

        # cartesian product of all arguments
        combined = itertools.product(*argument_lists) 

        # respect filters of Function
        # TODO apply function filter for valid sets
        filtered = filter(lambda x: True, combined)

        return filtered 

    def generate_sample(parameter: Parameter) -> Iterable[Variable]:
        """"""

        type_samples = []

        for partition in parameter.type.partitions:
            pass

        return type_samples
