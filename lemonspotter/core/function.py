"""
This module defines the function class which respresents functions from the specification.
"""

from typing import Mapping, Any, AbstractSet, Sequence, Callable, NamedTuple, Optional
from functools import lru_cache
import logging

from core.variable import Variable
from core.database import Database
from core.statement import FunctionStatement
from core.type import Type
from core.parameter import Parameter
from core.source import Source
from core.partition import Partition


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

        return self._json['name']

    @property
    def has_parameters(self) -> bool:
        return self._json['parameters']

    @property  # type: ignore
    @lru_cache()
    def parameters(self) -> Sequence[Parameter]:
        """This property provides access to the parameter list of this Function object."""

        return tuple(Parameter(self._db, parameter) for parameter in self._json['parameters'])

    @property
    def default_partition(self) -> Partition:
        """"""

        return Partition(self._db, self, self._json['partitions']['default'])

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


class FunctionSample:
    """"""

    def __init__(self, function: Function) -> None:
        self._function: Function = function
        self._return_variable: Variable = Variable(function.return_type)

        self._arguments: Optional[Sequence[Variable]] = None
        self._evaluator: Optional[Callable[[], bool]] = None

    @property
    def function(self) -> Function:
        """"""

        return self._function

    @property
    def return_variable(self) -> Variable:
        """"""
        
        return self._return_variable

    @property
    def arguments(self) -> Sequence[Variable]:
        """"""
        
        if self._arguments is None:
            return []

        return self._arguments

    @arguments.setter
    def arguments(self, arguments: Sequence[Variable]) -> None:
        """"""

        assert arguments is not None
        self._arguments = arguments

    @property
    def evaluator(self) -> Callable[[], bool]:
        """"""

        assert self._evaluator is not None
        return self._evaluator

    @evaluator.setter
    def evaluator(self, evaluator: Callable[[], bool]) -> None:
        """"""

        assert evaluator is not None
        self._evaluator = evaluator

    def generate_statement(self, source: Source) -> FunctionStatement:
        """
        Generates a compilable expression of the function with the given arguments.
        """

        self._return_variable.name = 'return_' + self._function.name 

        if self._return_variable.name in source.variables:
            raise NotImplementedError('Test if the variable already exists.')

        statement = ''
        statement += self.function.return_type.language_type + ' ' + self._return_variable.name
        statement += ' = '
        statement += self.function.name + '('

        # add arguments
        logging.debug('arguments %s', str(self._arguments))
        logging.debug('parameters %s', str(self.function.parameters))

        if self.function.has_parameters:
            for idx, (argument, parameter) in enumerate(zip(self._arguments, self.function.parameters)):
                mod = ''

                pointer_diff = argument.pointer_level - parameter.pointer_level
                if pointer_diff < 0:
                    # addressof &
                    mod += '&'

                elif pointer_diff > 0:
                    # dereference *
                    raise NotImplementedError

                statement += (mod + argument.name)

                if (idx + 1) != len(self._arguments):
                    statement += ', '

        statement += ');'

        return FunctionStatement(statement, {self._return_variable.name: self._return_variable})
