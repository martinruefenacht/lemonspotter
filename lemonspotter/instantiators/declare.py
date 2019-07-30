"""
This module contains the definition of the DefaultInstantiator.
"""

import logging
from typing import Iterable

from core.instantiator import Instantiator
from core.database import Database
from core.variable import Variable
from core.function import Function
from core.sample import FunctionSample


class DeclarationInstantiator(Instantiator):
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

        logging.debug('DeclarationInstantiator used for %s', function.name)

        sample = FunctionSample(function, function.default_partition)

        def evaluator() -> bool:
            raise NotImplementedError('DeclarationInstantiator only generates compilable ' +
                                      'code, not runnable.')

        sample.evaluator = evaluator

        # generate valid but empty arguments
        arguments = []

        for parameter in function.parameters:  # type: ignore
            variable = Variable(parameter.type, parameter.name)
            arguments.append(variable)

        sample.arguments = arguments

        return set([sample])
