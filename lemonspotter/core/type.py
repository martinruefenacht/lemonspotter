"""
Defines a type object of from library that can be included in Lemonspotter tests.
"""

from typing import Mapping, Any, Iterable, Optional
from functools import lru_cache
import logging

from core.database import Database
from core.partition import Partition


class Type:
    """
    This class represents the type abstraction from the specification.
    """

    def __init__(self, database: Database, json: Mapping[str, Any]) -> None:
        self._json = json
        self._database: Database = database

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

        return self._database.type_by_abstract_type[self._json['language_type']].language_type

    @property
    def printable(self) -> bool:
        """This property provides whether this is a C printable type."""

        if self._json['base_type']:
            return self._json.get('print_specifier', False)

        return self._database.type_by_abstract_type[self._json['language_type']].printable

    @property
    def print_specifier(self) -> str:
        """This property provides the C printf type specifier."""

        if self._json['base_type']:
            return self._json['print_specifier']

        return self._database.type_by_abstract_type[self._json['language_type']].print_specifier

    @property  # type: ignore
    @lru_cache()
    def partitions(self) -> Iterable[Partition]:
        """"""

        if 'partitions' in self._json:
            return [Partition(self._database, partition) for partition in self._json['partitions']]

        return []

    def validate(self, value: str) -> bool:
        """"""

        valid = any(partition.validate(value) for partition in self.partitions)  # type: ignore
        logging.debug('%s is valid with type %s: %s', value, self.name, str(valid))

        return valid

    @property
    def referencable(self) -> bool:
        """"""

        return 'reference' in self._json

    def reference(self) -> 'Type':
        """"""

        assert 'reference' in self._json

        return self._database.type_by_abstract_type[self._json['reference']]

    @property
    def dereferencable(self) -> bool:
        """"""

        return 'dereference' in self._json

    def dereference(self) -> 'Type':
        """"""

        assert 'dereference' in self._json

        return self._database.type_by_abstract_type[self._json['dereference']]
