"""
This module contains the definition of the DefaultSampler.
"""

import logging
from typing import Iterable, Sequence

from core.sampler import Sampler
from core.database import Database
from core.variable import Variable
from core.function import Function
from core.sample import FunctionSample


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

        argument_lists: Sequence[Sequence[Variable]] = []

        for parameter in function.parameters:
            type_samples = []

            for partition in parameter.partitions:
                # generate sampling pattern
                pass

            arguments.append(type_samples)

        # cartesian product of all arguments


        # generate valid arguments from function parameter types


        # respect filters of Function


        # TODO
        return [] 
