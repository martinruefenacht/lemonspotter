"""
This module contains the definition of the DefaultInstantiator.
"""

import logging
from typing import Set, Tuple, Dict

from core.instantiator import Instantiator
from core.database import Database
from core.variable import Variable
from core.parameter import Parameter

class DefaultInstantiator(Instantiator):
    """
    This class implements the DefaultInstantiator behaviour. It uses the default values from the
    specification types to create a single Variable.
    """

    def __init__(self, database: Database) -> None:
        super().__init__(database)

    def generate_variables(self, parameters: Tuple[Parameter]) -> Dict[str, Tuple[Tuple[Variable]]]:
        """This method generates a set of variables according to the parameter list."""

        variables = []

        for parameter in parameters:
            variables.append(self.generate_variable(parameter))

        return variables

    def generate_variable(self, parameter: Parameter) -> Set[Variable]:
        """This method outputs the list of variables generated from a parameter."""

        return set(Variable(parameter.type, parameter.name, parameter.type.default))
