"""
This module contains the definition of the DefaultSampler.
"""

import logging
from typing import Iterable, Mapping
from itertools import chain, product

from lemonspotter.core.sampler import Sampler
from lemonspotter.core.database import Database
from lemonspotter.core.variable import Variable
from lemonspotter.core.function import Function
from lemonspotter.core.argument import Argument
from lemonspotter.core.sample import FunctionSample
from lemonspotter.core.parameter import Parameter, Direction
from lemonspotter.core.partition import PartitionType


def cartesian_dict_product(inp):
    """
    https://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists
    """

    return (dict(zip(inp.keys(), values)) for values in product(*inp.values()))


class ValidSampler(Sampler):
    """
    """

    def __str__(self) -> str:
        return type(self).__name__

    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        """
        """

        logging.debug('generating samples of parameters for %s', function.name)

        if not (function.has_in_parameters or function.has_inout_parameters):
            return self._generate_empty_sample(function)

        arguments = {}
        for parameter in chain(function.in_parameters,
                               function.inout_parameters):  # type: ignore
            arguments[parameter.name] = self._generate_arguments(parameter)

        if not arguments:
            raise RuntimeError('No arguments generated from a function with parameters.')

        logging.debug('pre cartesian product: %s', arguments)

        # cartesian product of all arguments
        combined = cartesian_dict_product(arguments)
        logging.debug('prefiltering argument lists: %s', combined)

        # respect filters of Function
        def argument_filter(arguments: Mapping[Parameter, Argument]) -> bool:
            for sieve in function.filters:  # any sieve needs to be True
                # go through parameters/argument mapping, needs to match all requirements
                for parameter_name, argument in arguments.items():  # type: ignore
                    if sieve[parameter_name]['value'] == 'any':
                        continue

                    if sieve[parameter_name]['value'] != argument.variable.value:
                        break

                else:
                    # sieve applies
                    return True

            logging.debug('%s has no sieve allowed.', arguments)
            return False

        filtered = filter(argument_filter, combined)

        # convert to FunctionSample
        samples = set()

        for arguments in filtered:
            sample = FunctionSample(function, True, arguments)

            # function without parameters
            # note sample=sample is done to avoid late binding closure behaviour!
            def evaluator(sample=sample) -> bool:
                # todo use valid error lookup rule
                logging.debug('evaluator for function %s', function.name)
                logging.debug('sampler return variable %s', str(sample.return_variable))
                logging.debug('return variable %s == MPI_SUCCESS', sample.return_variable.value)

                return (sample.return_variable.value ==
                        Database().get_constant('MPI_SUCCESS').value)

            sample.evaluator = evaluator
            samples.add(sample)

        return samples

    def _generate_arguments(self, parameter: Parameter) -> Iterable[Argument]:
        """"""

        assert parameter.direction is not Direction.OUT

        arguments = set()

        # TODO partition should return str for value
        # it is in charge of interpreting PartitionType, not here
        # this should be in an object oriented pattern, not an large if block
        for partition in parameter.type.partitions:  # type: ignore
            if partition.type is PartitionType.LITERAL:
                name = f'{parameter.name}_arg_{partition.value}'

                arguments.add(Argument(Variable(parameter.type, name, partition.value)))

            elif partition.type is PartitionType.NUMERIC:
                name = f'{parameter.name}_arg_{partition.value}'

                arguments.add(Argument(Variable(parameter.type, name, partition.value)))

            elif partition.type is PartitionType.PREDEFINED:
                name = f'{parameter.name}_arg_{partition.value}'

                arguments.add(Argument(Variable(parameter.type,
                                                name,
                                                partition.value,
                                                predefined=True)))

            elif partition.type is PartitionType.CONSTANT:
                for constant in parameter.type.constants:
                    name = f'{parameter.name}_arg_{constant.name}'

                    arguments.add(Argument(constant.generate_variable(name)))

            else:
                logging.error(('Trying to generate variable from unknown partition'
                               ' type %s in ValidSampler.'),
                              partition.type)

        return arguments
