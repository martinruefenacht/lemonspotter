"""
"""

from typing import TYPE_CHECKING, Mapping, Any, Optional
import logging

from core.database import Database
from core.variable import Variable
from core.statement import ConditionStatement
if TYPE_CHECKING:
    from core.function import Function


class Partition:
    """
    This class represents the concept of a partition.
    """

    def __init__(self, database: Database, function: 'Function', json: Mapping[str, Any]) -> None:
        self._db = database
        self._function = function
        self._json = json
        self._return = json['_return']

    def __contains__(self, name: str) -> bool:
        """"""

        return self._json.get(name, False)

    def __getitem__(self, name: str) -> Mapping[str, str]:
        """"""

        return self._json[name]

    @property
    def return_symbol(self) -> str:
        """"""

        if self._return['type'] == 'constant':
            return self._return['constant']

        else:
            raise NotImplementedError('Partition return values other than constants not implemented.')

    @property
    def return_operand(self) -> Optional[str]:
        """"""

        return self._return.get('operand', None)

    def validate(self, variable: Variable) -> bool:
        """"""

        logging.debug('validating %s to partition.', variable.name)

        if self._return['type'] == 'constant':
            if self._return['operand'] == 'equal':
                return self._db.constants_by_name[self._return['constant']].value == variable.value

            else:
                raise NotImplementedError('Operands for _return other than "equal" are not implemented.')

        else:
            raise NotImplementedError('Types of _return other than Constant are not implemented.')
