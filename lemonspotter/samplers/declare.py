"""
This module contains the definition of the DefaultSampler.
"""

import logging
from typing import Iterable

from core.sampler import Sampler
from core.database import Database
from core.variable import Variable
from core.function import Function
from core.sample import FunctionSample


class DeclarationSampler(Sampler):
    """
    This class implements the DefaultSampler behaviour. It uses the default values from the
    specification types to create a single Variable.
    """

    def __str__(self) -> str:
        return type(self).__name__

    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        """
        """

        logging.debug('DeclarationSampler used for %s', function.name)

        def evaluator() -> bool:
            raise NotImplementedError('DeclarationSampler only generates compilable ' +
                                      'code, not runnable.')

        # generate valid but empty arguments
        arguments = []
        variables = set()

        for parameter in function.parameters:  # type: ignore
            variable = Variable(parameter.type, f'arg_{parameter.name}')

            # add variable to variable set
            variables.add(variable)

            logging.debug('declaring variable argument: %s', variable.name)
            arguments.append(variable)

        sample = FunctionSample(function, True, variables, arguments, evaluator)

        return set([sample])
