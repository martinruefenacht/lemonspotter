"""
This module defines the function class which respresents functions from the specification.
"""

from typing import Mapping, Any, AbstractSet, Sequence
from functools import lru_cache

from core.database import Database
from core.type import Type
from core.parameter import Parameter


class Function:
    """
    Defines an function object that can be included in Lemonspotter tests.
    """

    def __init__(self, database: Database, json: Mapping[str, Any]) -> None:
        """
        """

        self._db: Database = database
        self._json: Mapping[str, Any] = json

        self.properties: Mapping[str, Any] = {}

    def __repr__(self) -> str:
        """
        Defines informal string behavior for function type
        """

        return self._json['name']

    def __str__(self) -> str:
        """
        Defines formal string behavior for function type
        """

        return repr(self)

    @property
    def name(self) -> str:
        """This property provides access to the Function name."""

        assert self._json.get('name', None) is not None
        return self._json['name']

    @property
    def has_parameters(self) -> bool:
        """"""

        return self._json.get('parameters', False)

    @property  # type: ignore
    @lru_cache()
    def parameters(self) -> Sequence[Parameter]:
        """This property provides access to the parameter list of this Function object."""

        assert self._json.get('parameters', None) is not None
        return tuple(Parameter(self._db, parameter) for parameter in self._json['parameters'])

#    @property
#    def default_partition(self) -> Partition:
#        """"""
#
#        assert self._json.get('partitions', None) is not None
#        assert self._json['partitions'].get('default', None) is not None
#        return Partition(self._db, self, self._json['partitions']['default'])

    @property
    def return_type(self) -> Type:
        """This property provides the Type object of the return of this Function."""

        assert self._json.get('return', None) is not None
        return self._db.type_by_abstract_type[self._json['return']]

    @property  # type: ignore
    @lru_cache()
    def needs_any(self) -> AbstractSet['Function']:
        """This property provides access to the any set of needed Function objects."""

        assert self._json.get('needs_any', None) is not None
        subset = filter(lambda name: name in self._db.functions_by_name, self._json['needs_any'])

        return set(self._db.functions_by_name[func_name] for func_name in subset)

    @property  # type: ignore
    @lru_cache()
    def needs_all(self) -> AbstractSet['Function']:
        """This property provides access to the all set of needed Function objects."""

        assert self._json.get('needs_all', None) is not None
        subset = filter(lambda name: name in self._db.functions_by_name, self._json['needs_all'])

        return set(self._db.functions_by_name[func_name] for func_name in subset)

    @property  # type: ignore
    @lru_cache()
    def leads_any(self) -> AbstractSet['Function']:
        """This property provides access to the any set of lead Function objects."""

        assert self._json.get('leads_any', None) is not None
        subset = filter(lambda name: name in self._db.functions_by_name, self._json['leads_any'])

        return set(self._db.functions_by_name[func_name] for func_name in subset)

    @property  # type: ignore
    @lru_cache()
    def leads_all(self) -> AbstractSet['Function']:
        """This property provides access to the all set of lead the Function objects."""

        assert self._json.get('leads_all', None) is not None
        subset = filter(lambda name: name in self._db.functions_by_name, self._json['leads_all'])

        return set(self._db.functions_by_name[func_name] for func_name in subset)

    @property
    def present(self) -> bool:
        """"""

        return self.properties.get('present', False)
