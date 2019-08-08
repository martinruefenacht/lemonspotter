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

        logging.debug('generating samples of parameters for %s', function.name)

        if not function.parameters:
            # function without parameters
            def evaluator():
                return True

            logging.debug('%s has no arguments.', function.name)

            return {FunctionSample(function, True, {}, [], evaluator)}

        argument_lists = []

        for parameter in function.parameters:  # type: ignore
            argument_lists.append(self.generate_sample(parameter))

        # cartesian product of all arguments
        combined = set(itertools.product(*argument_lists))
        logging.debug('prefiltering argument lists: %s', str(combined))

        # respect filters of Function
        for argument_list in combined:
            # check whether argument list is allowed by function filter
            # TODO how do we do this?
            pass

        # TODO convert values to FunctionSample
        #logging.debug('generated samples %s', str(filtered))

        # create function sample for each argument list
        #FunctionSample(function, True, variables, arguments, evalator) 

        return []

    def generate_sample(self, parameter: Parameter) -> Iterable[Variable]:
        """"""

        type_samples = []

        # TODO partition should return str for value
        # it is in charge of interpreting PartitionType, not here
        for partition in parameter.type.partitions:  # type: ignore
            if partition.type is PartitionType.LITERAL:
                name = f'{parameter.name}_arg_{partition.value}'
                var = Variable(parameter.type, name, partition.value)

                type_samples.append(var)

            elif partition.type is PartitionType.NUMERIC:
                name = f'{parameter.name}_arg_{partition.value}'
                var = Variable(parameter.type, name, partition.value)

                type_samples.append(var)

            elif partition.type is PartitionType.PREDEFINED:
                name = f'{parameter.name}_arg_{partition.value}'
                var = Variable(parameter.type, name, partition.value)

                type_samples.append(var)

            else:
                logging.error('Trying to generate variable from unknown partition type in ValidSampler.' + str(partition.type))

        return type_samples
