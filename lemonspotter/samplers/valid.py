"""
This module contains the definition of the DefaultSampler.
"""

import logging
from typing import Iterable
import itertools

from lemonspotter.core.sampler import Sampler
from lemonspotter.core.database import Database
from lemonspotter.core.variable import Variable
from lemonspotter.core.function import Function
from lemonspotter.core.sample import FunctionSample
from lemonspotter.core.parameter import Parameter, Direction
from lemonspotter.core.partition import PartitionType


class ValidSampler(Sampler):
    """
    """

    def __str__(self) -> str:
        return type(self).__name__

    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        """
        """

        logging.debug('generating samples of parameters for %s', function.name)

        if not function.parameters:
            logging.debug('%s has no arguments.', function.name)

            sample = FunctionSample(function, True, {}, [])

            def evaluator(sample=sample) -> bool:
                return (sample.return_variable.value ==
                        Database().get_constant('MPI_SUCCESS').value)

            sample.evaluator = evaluator

            return {sample}

        argument_lists = []

        for parameter in function.parameters:  # type: ignore
            argument_lists.append(self.generate_sample(parameter))

        if not argument_lists:
            raise Exception('No arguments generated from a function with parameters.')

        logging.debug('pre cartesian product: %s', str(argument_lists))

        # cartesian product of all arguments
        combined = set(itertools.product(*argument_lists))
        logging.debug('prefiltering argument lists: %s', str(combined))

        # respect filters of Function
        def argument_filter(argument_list: Iterable) -> bool:
            for sieve in function.filters:  # any sieve needs to be True
                # go through parameters/argument mapping, needs to match all requirements
                for parameter, argument in zip(function.parameters, argument_list):  # type: ignore
                    if parameter.direction is Direction.OUT:
                        # note we don't write out arguments in function filters
                        continue

                    elif sieve[parameter.name]['value'] == 'any':
                        continue

                    elif sieve[parameter.name]['value'] != argument.value:
                        break

                else:
                    # sieve applies
                    return True

            else:
                logging.debug('%s has no sieve allowed.', argument_list)
                return False

        filtered = filter(argument_filter, combined)

        # convert to FunctionSample
        samples = set()

        for argument_list in filtered:
            sample = FunctionSample(function, True, set(argument_list), argument_list)

            # function without parameters
            # NOTE sample=sample is done to avoid late binding closure behaviour!
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

    def generate_sample(self, parameter: Parameter) -> Iterable[Variable]:
        """"""

        type_samples = []

        if parameter.direction == Direction.OUT:
            print(parameter.name)
            """
            CODE NEEDS TO BE IMPLEMENTED HERE
            """
            if parameter.type.referencable:
                nonref_var = Variable(parameter.type.dereference(),
                                      "nonref_"+parameter.name)
                var = Variable(parameter.type, parameter.name+'_out', "&"+nonref_var.name+"_out")

                type_samples.append(nonref_var)
                type_samples.append(var)

            else:
                # generate out variable
                var = Variable(parameter.type, parameter.name + '_out')

                type_samples.append(var)

            return type_samples

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
                var = Variable(parameter.type, name, partition.value, predefined=True)

                type_samples.append(var)

            elif partition.type is PartitionType.CONSTANT:
                for constant in parameter.type.constants:
                    name = f'{parameter.name}_arg_{constant.name}'
                    type_samples.append(constant.generate_variable(name))

            else:
                logging.error(('Trying to generate variable from unknown'
                               ' partition type in ValidSampler.') + str(partition.type))

        return type_samples
