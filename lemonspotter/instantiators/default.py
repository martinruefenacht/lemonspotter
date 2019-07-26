"""
This module contains the definition of the DefaultInstantiator.
"""

import logging
from typing import Iterable

from core.instantiator import Instantiator
from core.database import Database
from core.variable import Variable
from core.function import Function, FunctionSample


class DefaultInstantiator(Instantiator):
    """
    This class implements the DefaultInstantiator behaviour. It uses the default values from the
    specification types to create a single Variable.
    """

    def __init__(self, database: Database) -> None:
        super().__init__(database)

    def __str__(self) -> str:
        return type(self).__name__

    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        """
        """

        logging.debug('DefaultInstantiator used for %s.', function.name)

        sample = FunctionSample(function)

        def evaluator() -> bool:
            return function.default_partition.validate(sample.return_variable)
        sample.evaluator = evaluator

        if function.has_parameters:
            if function.default_partition:
                partition = function.default_partition
                arguments = []

                for parameter in function.parameters:  # type: ignore
                    if parameter.name not in partition:
                        raise RuntimeError('Found parameter which is not part of ' +
                                           'the default_partition.')

                    if partition[parameter.name]['type'] == 'literal':
                        arguments.append(Variable(parameter.type,
                                         parameter.name,
                                         partition[parameter.name]['literal']))

                    else:
                        raise NotImplementedError('Partition argument type is not literal.')

                sample.arguments = arguments

            else:
                raise NotImplementedError('no default partition, but parameters exist.')

                # arguments.append(Variable(parameter.type,
                #                  parameter.name,
                #                  parameter.type.default))

        return set([sample])
