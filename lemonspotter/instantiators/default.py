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
        
        # handle zero parameter functions
        # TODO this still has an expected partition result
        if not function.has_parameters:
            def tester() -> bool:
                function.default_partition 

            sample.return_variable
            sample.evaluator

        # does the function have a default parameter set
        default = function.default_parameters
        if default is not None:
            arguments: MutableSequence = []

            for parameter in default:
                #arguments.append(Variable(parameter.type, parameter.name, parameter.type.default))
                # TODO
                pass

            sample.arguments = arguments

            # create evaluator
            def tester() -> None:
                if default['_expected']['type'] == 'constant':
                    if sample.return_variable.value != self._db.constant_by_name[default['_expected']['name']]['value']:
                        return False
                    else:
                        return True
                else:
                    raise NotImplementedError('other return types not implemented')
            
            sample.evaluator = tester

        else:
            raise NotImplementedError('Function %s does not provide a default argument partition.', function.name)
            # TODO go through parameters looking for defaults

            # else go through types using defaults

            # else raise ERROR

        return set([sample])
