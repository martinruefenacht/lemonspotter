"""
This module contains the definition of the DefaultInstantiator.
"""

import logging
from typing import Iterable

from core.instantiator import Instantiator
from core.database import Database
from core.variable import Variable
from core.function import Function, FunctionSample


class ConstantExploringInstantiator(Instantiator):
    """
    """

    def __init__(self, database: Database) -> None:
        super().__init__(database)

    def __str__(self) -> str:
        return type(self).__name__

    def generate_samples(self, function: Function) -> Iterable[FunctionSample]:
        """
        """

        logging.debug('ConstantExploringInstantiator used for %s.', function.name)

        # TODO single partition does not work
        sample = FunctionSample(function, function.default_partition)

        if function.has_parameters:
            arguments = []

            for parameter in function.parameters:  # type: ignore
                pass

                # generate variable from parameter.partitions
                # need to link?

            sample.arguments = arguments

        def evaluator() -> bool:
            #return function.default_partition.validate(sample.return_variable)

            # 
            pass

        sample.evaluator = evaluator


        return set([sample])
