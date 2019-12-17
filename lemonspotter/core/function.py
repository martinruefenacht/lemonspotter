"""
This module defines the function class which respresents functions from the specification.
"""

from typing import Mapping, Any, AbstractSet, Sequence, Iterable

from lemonspotter.core.database import Database
from lemonspotter.core.type import Type
from lemonspotter.core.parameter import Parameter
from lemonspotter.core.parameter import Direction


class Function:
    """
    Defines an function object that can be included in Lemonspotter tests.
    """

    def __init__(self, json: Mapping[str, Any]) -> None:
        """
        """

        self._json: Mapping[str, Any] = json
        self.properties: Mapping[str, Any] = {}

        # cache
        self._parameters = None
        self._in_parameters = None
        self._inout_parameters = None
        self._out_parameters = None

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
            raise RuntimeError('Function name is not in JSON.')

        return self._json['name']

    @property
    def has_parameters(self) -> bool:
        """"""

        return 'parameters' in self._json

    @property
    def has_in_parameters(self) -> bool:
        """"""

        return len(self.in_parameters) > 0

    @property
    def has_inout_parameters(self) -> bool:
        """"""

        return len(self.inout_parameters) > 0

    @property
    def has_out_parameters(self) -> bool:
        """"""

        return len(self.out_parameters) > 0

    @property  # type: ignore
    def parameters(self) -> Sequence[Parameter]:
        """This property provides access to the parameter list of this Function object."""

        if 'parameters' not in self._json:
            raise RuntimeError('Parameters are not in JSON.')

        if self._parameters is None:
            self._parameters = tuple(Parameter(parameter)
                                     for parameter in self._json['parameters'])

        return self._parameters

    @property
    def in_parameters(self) -> Sequence[Parameter]:
        """
        Find all parameters which are with IN or INOUT parameters.
        """

        if self._in_parameters is None:
            self._in_parameters = tuple(parameter
                                        for parameter in self.parameters
                                        if parameter.direction is Direction.IN)

        return self._in_parameters

    @property
    def inout_parameters(self) -> Sequence[Parameter]:
        """
        Find all parameters which are with IN or INOUT parameters.
        """

        if self._inout_parameters is None:
            self._inout_parameters = tuple(parameter
                                           for parameter in self.parameters
                                           if parameter.direction is Direction.INOUT)

        return self._inout_parameters

    @property
    def out_parameters(self) -> Sequence[Parameter]:
        """
        Find all parameters which are either OUT or INOUT parameters.
        """

        if self._out_parameters is None:
            self._out_parameters = tuple(parameter
                                         for parameter in self.parameters
                                         if parameter.direction is Direction.OUT)

        return self._out_parameters

    @property
    def return_type(self) -> Type:
        """This property provides the Type object of the return of this Function."""

        if 'return' not in self._json:
            raise RuntimeError('Return is not in JSON.')

        return Database().get_type(self._json['return'])

    @property  # type: ignore
    def needs_any(self) -> AbstractSet['Function']:
        """This property provides access to the any set of needed Function objects."""

        if 'needs_any' not in self._json:
            raise RuntimeError('Needs any is not in JSON.')

        subset = filter(lambda name: Database().has_function(name), self._json['needs_any'])

        return set(Database().get_function(func_name) for func_name in subset)

    @property  # type: ignore
    def needs_all(self) -> AbstractSet['Function']:
        """This property provides access to the all set of needed Function objects."""

        if 'needs_all' not in self._json:
            raise RuntimeError('Needs all is not in JSON.')

        subset = filter(lambda name: Database().has_function(name), self._json['needs_all'])

        return set(Database().get_function(func_name) for func_name in subset)

    @property  # type: ignore
    def leads_any(self) -> AbstractSet['Function']:
        """This property provides access to the any set of lead Function objects."""

        if 'leads_any' not in self._json:
            raise RuntimeError('Leads any is not in JSON.')

        subset = filter(lambda name: Database().has_function(name), self._json['leads_any'])

        return set(Database().get_function(func_name) for func_name in subset)

    @property  # type: ignore
    def leads_all(self) -> AbstractSet['Function']:
        """This property provides access to the all set of lead the Function objects."""

        if 'leads_all' not in self._json:
            raise RuntimeError('Leads all is not in JSON.')

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
