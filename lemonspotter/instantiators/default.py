"""
This module contains the definition of the DefaultInstantiator.
"""

import logging
from typing import List

from core.database import Database
from core.variable import Variable
from core.parameter import Parameter

class DefaultInstantiator:
    """
    This class implements the DefaultInstantiator behaviour. It uses the default values from the
    specification types to create a single Variable.
    """

    def __init__(self, database: Database) -> None:
        self._database: Database = database

    def generate_variables(self, parameter: Parameter) -> List[Variable]:
        """This method outputs the list of variables generated from a parameter."""

        return [Variable(parameter.type, parameter.name, parameter.type.default)]
