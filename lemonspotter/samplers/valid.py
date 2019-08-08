"""
This module contains the definition of the DefaultSampler.
"""

import logging
from typing import Iterable
import itertools

from core.sampler import Sampler
from core.database import Database
from core.variable import Variable
from core.function import Function
from core.sample import FunctionSample
from core.parameter import Parameter
from core.partition import Partition, PartitionType


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

        argument_lists = []

        for parameter in function.parameters:  # type: ignore
            argument_lists.append(self.generate_sample(parameter))

        # cartesian product of all arguments
        combined = itertools.product(*argument_lists)

        # respect filters of Function
        # TODO apply function filter for valid sets
        filtered = filter(lambda x: True, combined)

        # TODO convert values to FunctionSample

        return filtered

    def generate_sample(self, parameter: Parameter) -> Iterable[Variable]:
        """"""

        type_samples = []

        for partition in parameter.type.partitions:  # type: ignore
            if partition.type == PartitionType.LITERAL:
                name = f'{parameter.name}_arg_{partition.value}'
                var = Variable(parameter.type, name, partition.value)

                type_samples.append(var)

            else:
                logging.error('Trying to generate variable from unknown partition type.')

        return type_samples
