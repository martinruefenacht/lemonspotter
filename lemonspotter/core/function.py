"""
This module defines the function class which respresents functions from the specification.
"""

from typing import Mapping, Any, AbstractSet, Sequence, Iterable
from functools import lru_cache

from lemonspotter.core.database import Database
from lemonspotter.core.type import Type
from lemonspotter.core.parameter import Parameter


class Function:
    """
    Defines an function object that can be included in Lemonspotter tests.
    """

    def __init__(self, json: Mapping[str, Any]) -> None:
        """
        """

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

        if 'name' not in self._json:
            raise Exception('Function name is not in JSON.')

        return self._json['name']

    @property
    def has_parameters(self) -> bool:
        """"""

        return self._json.get('parameters', False)

    @property  # type: ignore
    @lru_cache()
    def parameters(self) -> Sequence[Parameter]:
        """This property provides access to the parameter list of this Function object."""

        if 'parameters' not in self._json:
            raise Exception('Parameters are not in JSON.')

        return tuple(Parameter(parameter) for parameter in self._json['parameters'])

    @property
    def return_type(self) -> Type:
        """This property provides the Type object of the return of this Function."""

        if 'return' not in self._json:
            raise Exception('Return is not in JSON.')

        return Database().get_type(self._json['return'])

    @property
    def return_abstract_type(self) -> str:
        """
        """

        return self._json['return']

    @property  # type: ignore
    @lru_cache()
    def needs_any(self) -> AbstractSet['Function']:
        """This property provides access to the any set of needed Function objects."""

        if 'needs_any' not in self._json:
            raise Exception('Needs any is not in JSON.')

        subset = filter(lambda name: Database().has_function(name), self._json['needs_any'])

        return set(Database().get_function(func_name) for func_name in subset)

    @property  # type: ignore
    @lru_cache()
    def needs_all(self) -> AbstractSet['Function']:
        """This property provides access to the all set of needed Function objects."""

        if 'needs_all' not in self._json:
            raise Exception('Needs all is not in JSON.')

        subset = filter(lambda name: Database().has_function(name), self._json['needs_all'])

        return set(Database().get_function(func_name) for func_name in subset)

    @property  # type: ignore
    @lru_cache()
    def leads_any(self) -> AbstractSet['Function']:
        """This property provides access to the any set of lead Function objects."""

        if 'leads_any' not in self._json:
            raise Exception('Leads any is not in JSON.')

        subset = filter(lambda name: Database().has_function(name), self._json['leads_any'])

        return set(Database().get_function(func_name) for func_name in subset)

    @property  # type: ignore
    @lru_cache()
    def leads_all(self) -> AbstractSet['Function']:
        """This property provides access to the all set of lead the Function objects."""

        if 'leads_all' not in self._json:
            raise Exception('Leads all is not in JSON.')

        subset = filter(lambda name: Database().has_function(name), self._json['leads_all'])

        return set(Database().get_function(func_name) for func_name in subset)

    @property
    def present(self) -> bool:
        """"""

        return self.properties.get('present', False)

    @property
    def filters(self) -> Iterable[Mapping[str, Any]]:
        """"""

        return self._json['filters'] if 'filters' in self._json else []
