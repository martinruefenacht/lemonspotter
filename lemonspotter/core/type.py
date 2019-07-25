"""
Defines a type object of from library that can be included in Lemonspotter tests.
"""

from typing import Dict, Any, List
import logging

from core.database import Database

class Type:
    """
    This class represents the type abstraction from the specification.
    """

    def __init__(self, database: Database, json: Dict[str, Any]) -> None:
        self._json = json
        self._database: Database = database

        self._partitions: List[Dict] = []

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

        logging.debug('performing recursive lookup of language type.')
        return self._database.type_by_abstract_type[self._json['language_type']].language_type

    @property
    def printable(self) -> bool:
        """This property provides whether this is a C printable type."""

        if self._json['base_type']:
            return self._json['printable']

        logging.debug('performing recursive lookup of printable.')
        return self._database.type_by_abstract_type[self._json['language_type']].printable

    @property
    def print_specifier(self):
        """This property provides the C printf type specifier."""

        if self._json['base_type']:
            return self._json['print_specifier']

        logging.debug('performing recursive lookup of print specifier.')
        return self._database.type_by_abstract_type[self._json['language_type']].print_specifier
