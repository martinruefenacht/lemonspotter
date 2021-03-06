"""
Defines a type object of from library that can be included in Lemonspotter tests.
"""

import logging
from functools import lru_cache
from typing import TYPE_CHECKING, Mapping, Any, Iterable

from lemonspotter.core.database import Database
from lemonspotter.core.partition import Partition

if TYPE_CHECKING:
    from lemonspotter.core.constant import Constant  # noqa


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

        return Database().get_type(self._json['language_type']).language_type

    @property
    def printable(self) -> bool:
        """This property provides whether this is a C printable type."""

        if self._json['base_type']:
            return self._json.get('print_specifier', False)

        return Database().get_type(self._json['language_type']).printable

    @property
    def print_specifier(self) -> str:
        """This property provides the C printf type specifier."""

        if self._json['base_type']:
            return self._json['print_specifier']

        return Database().get_type(self._json['language_type']).print_specifier

    @property
    def constants(self) -> Iterable['Constant']:
        """"""

        return Database().get_constants(self.abstract_type)

    @property  # type: ignore
    @lru_cache()
    def partitions(self) -> Iterable[Partition]:
        """"""

        if 'partitions' in self._json:
            return [Partition(Database(), partition) for partition in self._json['partitions']]

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

        if 'reference' not in self._json:
            raise Exception(f'Type {self._json["name"]} cannot be referenced.')

        return Database().get_type(self._json['reference'])

    @property
    def dereferencable(self) -> bool:
        """"""

        return 'dereference' in self._json

    def dereference(self) -> 'Type':
        """"""

        if 'dereference' not in self._json:
            raise Exception(f'Type {self._json["name"]} cannot be dereferenced.')

        return Database().get_type(self._json['dereference'])
