"""
This module contains the class definition of Parameter.
"""

from typing import Dict, Any, Optional
from enum import Enum

from lemonspotter.core.database import Database
from lemonspotter.core.type import Type


class Direction(Enum):
    IN = 'in'
    OUT = 'out'
    INOUT = 'inout'


class Parameter:
    """
    This class represents parameters of Function objects translated from the specification.
    """

    def __init__(self, json: Dict[str, Any]):
        self._json = json

    @property
    def name(self) -> str:
        """This property provides the name of the Parameter."""

        if 'name' not in self._json:
            raise Exception('Name is not in JSON.')

        return self._json['name']

    @property
    def type(self) -> Type:
        """This property provides the Type object of the abstract type of this Parameter."""

        if 'abstract_type' not in self._json:
            raise Exception('Abstract type is not in JSON.')

        return Database().get_type(self._json['abstract_type'])

    @property
    def direction(self) -> Direction:
        """This property provides the direction of the Parameter."""

        if 'direction' not in self._json:
            raise Exception('Direction is not in JSON.')

        return Direction(self._json['direction'])

    @property
    def length(self) -> Optional[str]:
        """
        This property, if not None, provides the length of the parameter.
        """

        return self._json.get('length', None)
