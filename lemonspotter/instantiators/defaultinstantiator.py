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

    def generate_variable(self, parameter: Parameter) -> Variable:
        if isinstance(parameter, Parameter):
            raise NotImplementedError

        else:
            logging.warning('using temporary DefaultInstantiator path for parameter dict')

            logging.info('parameter ' + str(parameter))

            if parameter['direction'] == 'out': 
                variable = Variable(self._database.type_by_abstract_type[parameter['abstract_type']],
                    parameter['name'])

            else:
                variable = Variable(self._database.type_by_abstract_type[parameter['abstract_type']],
                    parameter['name'],
                    self._database.type_by_abstract_type[parameter['abstract_type']].default)

            return variable
