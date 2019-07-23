"""
"""

import logging
from typing import List

from core.database import Database
from core.variable import Variable
from core.parameter import Parameter

class DefaultInstantiator:
    """
    """

    def __init__(self, database: Database) -> None:
        self._database: Database = database

    def generate_variable(self, parameter: Parameter) -> List[Variable]:
        return [Variable(parameter.type, parameter.name)]
