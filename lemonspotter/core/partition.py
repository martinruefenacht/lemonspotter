"""
"""

from typing import Mapping, Any, Optional
from enum import Enum

from lemonspotter.core.database import Database


class Operand(Enum):
    EQUAL = 'equal'
    UNEQUAL = 'unequal'

    GREATER_THAN = 'greater_than'
    LESS_THAN = 'less_than'

    GREATER_THAN_OR_EQUAL = 'greater_than_or_equal'
    LESS_THAN_OR_EQUAL = 'less_than_or_equal'

    @classmethod
    def inverse(cls, operand: 'Operand') -> 'Operand':
        """"""

        inverses = {
                    cls.EQUAL:                 cls.UNEQUAL,
                    cls.UNEQUAL:               cls.EQUAL,

                    cls.GREATER_THAN:          cls.LESS_THAN_OR_EQUAL,
                    cls.LESS_THAN:             cls.GREATER_THAN_OR_EQUAL,

                    cls.GREATER_THAN_OR_EQUAL: cls.LESS_THAN,
                    cls.LESS_THAN_OR_EQUAL:    cls.GREATER_THAN
                   }

        return inverses[operand]

    @classmethod
    def symbol(cls, operand: 'Operand') -> str:
        """"""

        symbols = {
                    cls.EQUAL:                  '==',
                    cls.UNEQUAL:                '!=',
                    cls.GREATER_THAN:           '>',
                    cls.LESS_THAN:              '<',
                    cls.GREATER_THAN_OR_EQUAL:  '<=',
                    cls.LESS_THAN_OR_EQUAL:     '>='
                  }

        return symbols[operand]


# TODO should be multiple subclasses of Partition
class PartitionType(Enum):
    NUMERIC = 'numeric'
    LITERAL = 'literal'
    PREDEFINED = 'predefined'
    RANGE = 'range'
    CONSTANT = 'constant'
    CREATION = 'creation'


class Partition:
    """
    This class represents the concept of a partition.
    """

    def __init__(self, database: Database, json: Mapping[str, Any]) -> None:
        self._db = database
        self._json = json

    def __contains__(self, name: str) -> bool:
        """"""

        return self._json.get(name, False)

    def __getitem__(self, name: str) -> Mapping[str, str]:
        """"""

        return self._json[name]

    @property
    def type(self) -> PartitionType:
        """"""

        return PartitionType(self._json['type'])

    @property
    def value(self) -> Optional[str]:
        """"""

        return self._json.get('value', None)

#    def validate(self, variable: Variable) -> bool:
#        """"""
#
#        if self._return['type'] == 'constant':
#            if Operand(self.return_operand) == Operand.EQUAL:
#                return (self._db.constants_by_name[self._return['constant']].value ==
#                        variable.value)
#
#            else:
#                raise NotImplementedError(('Operands for _return other than "equal"
#                                            are not implemented.'))
#
#        else:
#            raise NotImplementedError('Types of _return other than Constant are not implemented.')

#    @property
#    def return_symbol(self) -> str:
#        """"""
#
#        if self._return['type'] == 'constant':
#            return self._return['constant']
#
#        else:
#            raise NotImplementedError(('Partition return values other than constants
#                                        not implemented.'))

#    @property
#    def return_operand(self) -> Operand:
#        """"""
#
#        operand = self._return.get('operand', None)
#
#        logging.debug('converted from "%s" to %s', operand, Operand(operand))
#        return Operand(operand)

#    def generate_statement(self, return_name: str) -> Optional[ConditionStatement]:
#        """"""
#
#        if self._json['_return']['type'] == 'free':
#            return None
#
#        # generate condition statement
#        inverse_op = Operand.symbol(Operand.inverse(self.return_operand))
#        statement = f'{return_name} {inverse_op} {self.return_symbol}'
#        return ConditionStatement(statement)
