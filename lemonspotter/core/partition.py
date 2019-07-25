"""
"""

from typing import TYPE_CHECKING, Mapping, Any, Sequence
import logging

from core.database import Database
from core.variable import Variable   

if TYPE_CHECKING:
    from core.function import Function

class Partition:
    """
    """

    def __init__(self, database: Database, function: 'Function', json: Mapping[str, Any]) -> None:
        self._database = database
        self._function = function
        self._json = json
        self._return = json['_return']

    def __contains__(self, name: str) -> bool:
        """"""

        return self._json.get(name, False)

    def __getitem__(self, name: str) -> Mapping[str, str]:
        """"""

        return self._json[name]

    def validate(self, variable: Variable) -> bool:
        """"""

        if self._return['type'] == 'constant':
            return self._database.constants_by_name[self._return['constant']].value == variable.value

        else:
            raise NotImplementedError
