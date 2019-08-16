"""
Defines a type object of from library that can be included in Lemonspotter tests.
"""

from typing import TYPE_CHECKING, Mapping, Any, Iterable
if TYPE_CHECKING:
    from core.constant import Constant
import logging

from core.database import Database

class Type:
    """
    This class represents the type abstraction from the specification.
    """

    def __init__(self, json: Mapping[str, Any]) -> None:
        self._json = json

        self._partitions: Iterable[Mapping] = []

    @property
    def default(self) -> str:
        """This property provides the default value of the Type."""

        return self._json['default']

    @property
    def name(self) -> str:
        """This property provides the Type name."""

        return self._json['name']

    @property
    def abstract_type(self) -> str:
        """This property provides the abstract type name."""

        return self._json['abstract_type']

    @property
    def language_type(self) -> str:
        """This property provides the language type name."""

        if self._json['base_type']:
            return self._json['language_type']

        return Database().type_by_abstract_type[self._json['language_type']].language_type

    @property
    def printable(self) -> bool:
        """This property provides whether this is a C printable type."""

        if self._json['base_type']:
            return self._json['printable']

        return Database().type_by_abstract_type[self._json['language_type']].printable

    @property
    def print_specifier(self) -> str:
        """This property provides the C printf type specifier."""

        if self._json['base_type']:
            return self._json['print_specifier']

        return Database().type_by_abstract_type[self._json['language_type']].print_specifier

    @property
    def constants(self) -> Iterable['Constant']:
        """"""
        
        return Database().constants_by_abstract_type[self.abstract_type]
