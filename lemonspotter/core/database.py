"""
This module defines the Database class.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Set, Dict, List
if TYPE_CHECKING:
    from core.function import Function
    from core.constant import Constant
    from core.type import Type


class Database:
    """
    This class stores all functions, types, and constants read in from
     the JSON database.
    """

    def __init__(self) -> None:
        self.functions: Set[Function] = set()
        self.constants: Set[Constant] = set()
        self.types: Set['Type'] = set()

        self.functions_by_name: Dict[str, Function] = {}
        self.constants_by_abstract_type: Dict[str, List[Constant]] = {}
        self.type_by_abstract_type: Dict[str, Type] = {}

    def add_constant(self, constant: Constant) -> None:
        """
        Adds a constant to the database.
        """

        # add to set of constants
        self.constants.add(constant)

        # add to lookup
        if constant.type.abstract_type not in self.constants_by_abstract_type:
            self.constants_by_abstract_type[constant.type.abstract_type] = []

        self.constants_by_abstract_type[constant.type.abstract_type].append(constant)

    def add_function(self, function: Function) -> None:
        """
        Adds a function to the database and adds it to the lookup by name.
        """

        # add to set of functions
        self.functions.add(function)

        # add to function lookup
        self.functions_by_name[function.name] = function

    def add_type(self, kind: Type) -> None:
        """
        Adds a type to the database and adds it to the lookup by abstract type.
        """

        # add to set of types
        self.types.add(kind)

        # add to dictionary of types
        self.type_by_abstract_type[kind.abstract_type] = kind
