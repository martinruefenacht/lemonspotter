"""
This module contains the definition of the DefaultSampler.
"""

import logging
from typing import Sequence, Iterable
from itertools import chain

from lemonspotter.core.parameter import Direction
from lemonspotter.core.sampler import Sampler
from lemonspotter.core.variable import Variable
from lemonspotter.core.function import Function
from lemonspotter.core.sample import FunctionSample
from lemonspotter.core.parameter import Parameter
from lemonspotter.core.argument import Argument


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
        arguments = {}

        for parameter in chain(function.in_parameters,
                               function.inout_parameters):  # type: ignore
            arguments[parameter.name] = self._generate_argument(parameter)

        sample = FunctionSample(function, True, arguments, evaluator)

        return set([sample])

    @classmethod
    def _generate_argument(cls, parameter: Parameter) -> Argument:
        """
        Generate all variables required for this parameter.
        """

        assert parameter.direction is not Direction.OUT

        return Argument(Variable(parameter.type, f'arg_{parameter.name}'))
