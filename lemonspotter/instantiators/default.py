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

    def generate_variable(self, parameter: Parameter) -> Variable:
        if isinstance(parameter, Parameter):
            return Variable(parameter.type, parameter.name)
