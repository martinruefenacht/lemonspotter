"""
This module defines the Database class.
"""

from typing import Set

from core.function import Function
from core.type import Type
from core.constant import Constant

class Database:
    """
    This class stores all functions, types, and constants read in from
     the JSON database.
    """

    def __init__(self) -> None:
        self.functions: Set[Function] = set()
        self.constants: Set[Constant] = set()
        self.types: Set[Type] = set()

        self.functions_by_name = {}
        self.constants_by_abstract_type = {}
        self.types_by_abstract_type = {}

    def add_constant(self, constant: Constant) -> None:
        """
        Adds a constant to the database.
        """

        # add to set of constants
        self.constants.add(constant)

        # add to lookup
        if constant.abstract_type not in self.constants_by_abstract_type:
            self.constants_by_abstract_type[constant.abstract_type] = []

        self.constants_by_abstract_type[constant.abstract_type].append(constant)

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
        self.types_by_abstract_type[kind.abstract_type] = kind