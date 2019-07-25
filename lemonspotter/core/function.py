"""
This module defines the function class which respresents functions from the specification.
"""

from typing import Mapping, Any, AbstractSet, Sequence, Callable
from functools import lru_cache

from core.variable import Variable
from core.database import Database
from core.statement import FunctionStatement
from core.type import Type
from core.parameter import Parameter


class FunctionSample:
    def __init__(self, function: 'Function', arguments: Sequence[Variable], evaluator: Callable[[], None]):
        self._function = function
        self._arguments = arguments
        self._evaluator = evaluator


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

    def generate_function_statement(self, arguments: Sequence[Variable],
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

    @property  # type: ignore
    @lru_cache()
    def parameters(self) -> Sequence[Parameter]:
        """This property provides access to the parameter list of this Function object."""

        return tuple(Parameter(self._db, parameter) for parameter in self._json['parameters'])

    @property
    def return_type(self) -> Type:
        """This property provides the Type object of the return of this Function."""

        return self._db.type_by_abstract_type[self._json['return']]

    @property  # type: ignore
    @lru_cache()
    def needs_any(self) -> AbstractSet['Function']:
        """This property provides access to the any set of needed Function objects."""

        subset = filter(lambda name: name in self._db.functions_by_name, self._json['needs_any'])

        return set(self._db.functions_by_name[func_name] for func_name in subset)

    @property  # type: ignore
    @lru_cache()
    def needs_all(self) -> AbstractSet['Function']:
        """This property provides access to the all set of needed Function objects."""

        subset = filter(lambda name: name in self._db.functions_by_name, self._json['needs_all'])

        return set(self._db.functions_by_name[func_name] for func_name in subset)

    @property  # type: ignore
    @lru_cache()
    def leads_any(self) -> AbstractSet['Function']:
        """This property provides access to the any set of lead Function objects."""

        subset = filter(lambda name: name in self._db.functions_by_name, self._json['leads_any'])

        return set(self._db.functions_by_name[func_name] for func_name in subset)

    @property  # type: ignore
    @lru_cache()
    def leads_all(self) -> AbstractSet['Function']:
        """This property provides access to the all set of lead the Function objects."""

        subset = filter(lambda name: name in self._db.functions_by_name, self._json['leads_all'])

        return set(self._db.functions_by_name[func_name] for func_name in subset)

    @property
    def present(self) -> bool:
        """"""

        return self.properties.get('present', False)


