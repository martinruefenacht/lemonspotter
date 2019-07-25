"""
This module contains the class definition of Parameter.
"""

from typing import Dict, Any

from core.database import Database
from core.type import Type

class Parameter:
    """
    This class represents parameters of Function objects translated from the specification.
    """

    def __init__(self, database: Database, json: Dict[str, Any]):
        self._database = database
        self._json = json

    @property
    def name(self) -> str:
        """This property provides the name of the Parameter."""

        return self._json['name']

    @property
    def type(self) -> Type:
        """This property provides the Type object of the abstract type of this Parameter."""

        return self._database.type_by_abstract_type[self._json['abstract_type']]

    @property
    def pointer_level(self) -> int:
        """This property provides the pointer level of the Parameter."""

        return int(self._json['pointer'])

    @property
    def direction(self) -> str:
        """This property provides the direction of the Parameter."""

        return self._json['direction']
