"""
This module defines the Database class.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Set, Dict, List, Mapping, Iterable
if TYPE_CHECKING:
    from lemonspotter.core.function import Function
    from lemonspotter.core.constant import Constant
    from lemonspotter.core.type import Type


class _Singleton(type):
    _instances: Mapping[_Singleton, _Singleton] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, *kwargs)

        return cls._instances[cls]


class Database(metaclass=_Singleton):
    """
    This class stores all functions, types, and constants read in from
    the JSON database.
    """

    def __init__(self) -> None:
        self._functions: Set[Function] = set()
        self._constants: Set[Constant] = set()
        self._types: Set[Type] = set()

        self._functions_by_name: Dict[str, Function] = {}
        self._constants_by_abstract_type: Dict[str, List[Constant]] = {}
        self._constants_by_name: Dict[str, Constant] = {}
        self._type_by_abstract_type: Dict[str, Type] = {}

    def add_constant(self, constant: Constant) -> None:
        """
        Adds a constant to the database.
        """

        # add to set of constants
        self._constants.add(constant)

        # add to lookups
        if constant.type.abstract_type not in self._constants_by_abstract_type:
            self._constants_by_abstract_type[constant.type.abstract_type] = []

        self._constants_by_abstract_type[constant.type.abstract_type].append(constant)
        self._constants_by_name[constant.name] = constant

    def get_constants(self, abstract_type: str = None) -> Iterable[Constant]:
        """"""

        if abstract_type is None:
            return self._constants

        elif abstract_type not in self._constants_by_abstract_type:
            raise Exception(f'''abstract type {abstract_type} not in
                              "constants by abstract type" look up.''')

        return self._constants_by_abstract_type[abstract_type]

    def get_constant(self, name: str) -> Constant:
        """"""

        if name not in self._constants_by_name:
            raise Exception(f'Constant {name} not in "constants by name" look up.')

        return self._constants_by_name[name]

    def add_function(self, function: Function) -> None:
        """
        Adds a function to the database and adds it to the lookup by name.
        """

        # add to set of functions
        self._functions.add(function)

        # add to function lookup
        self._functions_by_name[function.name] = function

    def get_functions(self) -> Iterable[Function]:
        """"""

        return self._functions

    def get_function(self, name: str) -> Function:
        """"""

        if name not in self._functions_by_name:
            raise Exception(f'Function {name} not in "functions by name" look up.')

        return self._functions_by_name[name]

    def has_function(self, name: str) -> bool:
        """"""

        return name in self._functions_by_name

    def add_type(self, kind: Type) -> None:
        """
        Adds a type to the database and adds it to the lookup by abstract type.
        """

        # add to set of types
        self._types.add(kind)

        # add to dictionary of types
        self._type_by_abstract_type[kind.abstract_type] = kind

    def get_type(self, abstract_type: str) -> Type:
        """"""

        return self._type_by_abstract_type[abstract_type]
