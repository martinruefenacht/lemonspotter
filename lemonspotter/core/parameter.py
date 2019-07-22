"""
"""

from typing import List, Dict

from core.database import Database
from core.type import Type

class Parameter:
    """
    """

    def __init__(self, database: Database, json: Dict[str, str]):
        """
        """

        self._database = database
        self._json = json

    @property
    def name(self) -> str:
        return self._json['name']

    @property
    def type(self) -> Type:
        return self._database.type_by_abstract_type[self._json['abstract_type']]

    @property
    def pointer_level(self) -> int:
        return int(self._json['pointer'])

    @property
    def direction(self) -> str:
        return self._json['direction']
