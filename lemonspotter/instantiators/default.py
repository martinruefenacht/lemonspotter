"""
This module contains the definition of the DefaultInstantiator.
"""

import logging
from typing import Set, Tuple, Iterable, MutableSequence

from core.instantiator import Instantiator
from core.database import Database
from core.variable import Variable
from core.parameter import Parameter
from core.function import Function, FunctionSample
from core.source import Source


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

        sample = FunctionSample(function)

        def evaluator() -> bool:
            return function.default_partition.validate(sample.return_variable)
        sample.evaluator = evaluator

        if function.has_parameters:
            if function.default_partition:
                partition = function.default_partition
                arguments = []

                for parameter in function.parameters:
                    if parameter.name not in partition:
                        raise RuntimeError('Found parameter which is not part of the default_partition.')

                    if partition[parameter.name]['type'] == 'literal':
                        arguments.append(Variable(parameter.type, parameter.name, partition[parameter.name]['literal']))

                    else:
                        raise NotImplementedError('Partition argument type is not literal.')

                sample.arguments = arguments

            else:
                raise NotImplementedError('no default partition, but parameters exist.')

#            for parameter in default:
#                #arguments.append(Variable(parameter.type, parameter.name, parameter.type.default))
#                # TODO
#                pass
#
#            sample.arguments = arguments
#
#            # create evaluator
#            def evaluator() -> bool:
#
#                if default['_expected']['type'] == 'constant':
#                    if sample.return_variable.value != self._db.constant_by_name[default['_expected']['name']]['value']:
#                        return False
#                    else:
#                        return True
#                else:
#                    raise NotImplementedError('other return types not implemented')
#            
#            sample.evaluator = tester
#
#        else:
#            raise NotImplementedError('Function %s does not provide a default argument partition.', function.name)
#            # TODO go through parameters looking for defaults
#
#            # else go through types using defaults
#
#            # else raise ERROR

        return set([sample])
