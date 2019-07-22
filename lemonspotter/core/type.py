"""
Defines a type object of from library that can be included in Lemonspotter tests.
"""

from typing import Dict, Any, List
import logging

from core.database import Database

class Type:
    """
    """

    def __init__(self, database: Database, json: Dict[str, Any]):
        """
        """

        self._json = json
        self._database: Database = database

        self._partitions: List[Dict] = []

    @property
    def base_type(self) -> bool:
        return self._json['base_type']

    @property
    def default(self) -> str:
        return self._json['default']

    @property
    def name(self) -> str:
        return self._json['name']

    @property
    def type(self) -> 'Type':
        logging.warning('Type.type -> Type makes no sense')
        return self._database.type_by_abstract_type[self.abstract_type]

    @property
    def abstract_type(self) -> str:
        return self._json['abstract_type']

    @property
    def language_type(self) -> str:
        if self._json['base_type']:
            return self._json['language_type']

        else:
            return self._database.type_by_abstract_type[self._json['language_type']].language_type

    @property
    def printable(self) -> bool:
        if self.base_type:
            return self._json['printable']

        else:
            return self._database.type_by_abstract_type[self._json['language_type']].printable

    @property
    def print_specifier(self):
        if self.base_type:
            return self._json['print_specifier']

        else:
            return self._database.type_by_abstract_type[self._json['language_type']].print_specifier

    def convert(self, string: str) -> Any:
        """

        """
        
        if self.language_type == 'int':
            return int(string)

        elif self.language_type == 'double' or self.language_type == 'float':
            return float(string)

        else:
            logging.error('unrecognized language type in Python.')
            raise RuntimeError('unrecognized')
