"""
This module contains the class definition of Parameter.
"""

from typing import Dict, Any
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

        assert 'name' in self._json
        return self._json['name']

    @property
    def type(self) -> Type:
        """This property provides the Type object of the abstract type of this Parameter."""

        assert 'abstract_type' in self._json
        return Database().get_type(self._json['abstract_type'])

    @property
    def direction(self) -> Direction:
        """This property provides the direction of the Parameter."""

        assert 'direction' in self._json
        return Direction(self._json['direction'])
