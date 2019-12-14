"""
This module contains the definition of the DefaultSampler.
"""

import logging
from typing import Iterable

from lemonspotter.core.parameter import Parameter, Direction
from lemonspotter.core.sampler import Sampler
from lemonspotter.core.variable import Variable
from lemonspotter.core.function import Function
from lemonspotter.core.sample import FunctionSample


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
            if parameter.direction == Direction.OUT and parameter.type.dereferencable:
                mem_alloc = f'malloc(sizeof({parameter.type.dereference().language_type}))'

                variable = Variable(parameter.type, f'arg_{parameter.name}', mem_alloc)
                variables.add(variable)
            else:
                variable = Variable(parameter.type, f'arg_{parameter.name}')
                variables.add(variable)


            logging.debug('declaring variable argument: %s', variable.name)
            arguments.append(variable)

        sample = FunctionSample(function, True, variables, arguments, evaluator)

        return set([sample])
