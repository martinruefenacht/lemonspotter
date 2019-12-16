"""
This module contains the definition of the DefaultSampler.
"""

import logging
from typing import Iterable

from lemonspotter.core.parameter import Direction
from lemonspotter.core.sampler import Sampler
from lemonspotter.core.variable import Variable
from lemonspotter.core.function import Function
from lemonspotter.core.sample import FunctionSample
from lemonspotter.core.parameter import Parameter


class DeclarationSampler(Sampler):
    """
    This class implements the DefaultSampler behaviour. It uses the default values from the
    specification types to create a single Variable.
    """

    def __str__(self) -> str:
        return type(self).__name__

    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        """
        Generate a FunctionSample which correctly declares everything such
        that it is able to be used to build a source fragment.
        """

        logging.debug('DeclarationSampler used for %s', function.name)

        def evaluator() -> bool:
            raise NotImplementedError('DeclarationSampler only generates compilable ' +
                                      'code, not runnable.')

        # generate valid but empty arguments
        arguments = []

        for parameter in function.parameters:  # type: ignore
            variables = self._generate_argument(parameter)

            logging.debug('declaring variable argument: %s', variables[0].name)
            arguments.append(variables[0])

        sample = FunctionSample(function, True, variables, arguments, evaluator)

        return set([sample])

    @classmethod
    def _generate_argument(cls, parameter: Parameter) -> Iterable[Variable]:
        """
        Generate all variables required for this parameter.
        """

        assert parameter.direction is not Direction.OUT

        variables = []

        variable = Variable(parameter.type, f'arg_{parameter.name}')
        variables.append(variable)

        return variables
