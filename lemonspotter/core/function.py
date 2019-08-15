"""
This module defines the function class which respresents functions from the specification.
"""

from typing import List, Dict, Any, Set, Optional

from core.variable import Variable
from core.database import Database
from core.statement import FunctionStatement
from core.type import Type
from core.parameter import Parameter

class Function:
    """
    Defines an function object that can be included in Lemonspotter tests.
    """

    def __init__(self, json: Dict[str, Any]) -> None:
        """
        """

        self._json: Dict[str, Any] = json

        self.properties: Dict[str, Any] = {}

        self._cached_parameters: Optional[List[Parameter]] = None

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

    def generate_function_statement(self, arguments: List[Variable],
                                    return_name: str) -> FunctionStatement:
        """
        Generates a compilable expression of the function with the given arguments.
        """

        statement = ''

        statement += self.return_type.language_type + ' ' + return_name

        return_variable = Variable(self.return_type, return_name)

        statement += ' = '
        statement += self.name + '('

        # add arguments
        for idx, (argument, parameter) in enumerate(zip(arguments, self.parameters)):
            mod = ''

            pointer_diff = argument.pointer_level - parameter.pointer_level
            if pointer_diff < 0:
                # addressof &
                mod += '&'

            elif pointer_diff > 0:
                # dereference *
                raise NotImplementedError

            statement += (mod + argument.name)

            if (idx + 1) != len(arguments):
                statement += ', '

        statement += ');'

        return FunctionStatement(statement, {return_name: return_variable})

    @property
    def name(self) -> str:
        """This property provides access to the Function name."""

        return self._json['name']

    @property
    def parameters(self) -> List[Parameter]:
        """This property provides access to the parameter list of this Function object."""

        if self._cached_parameters is None:
            self._cached_parameters = [Parameter(parameter)
                                       for parameter in self._json['parameters']]

        return self._cached_parameters

    @property
    def return_type(self) -> Type:
        """This property provides the Type object of the return of this Function."""

        return Database().type_by_abstract_type[self._json['return']]

    @property
    def needs_any(self) -> Set['Function']:
        """This property provides access to the any set of needed Function objects."""

        return set(Database().functions_by_name[func_name] for func_name in self._json['needs_any'])

    @property
    def needs_all(self) -> Set['Function']:
        """This property provides access to the all set of needed Function objects."""

        return set(Database().functions_by_name[func_name] for func_name in self._json['needs_all'])

    @property
    def leads_any(self) -> Set['Function']:
        """This property provides access to the any set of lead Function objects."""

        return set(Database().functions_by_name[func_name] for func_name in self._json['leads_any'])

    @property
    def leads_all(self) -> Set['Function']:
        """This property provides access to the all set of lead the Function objects."""

        return set(Database().functions_by_name[func_name] for func_name in self._json['leads_all'])
