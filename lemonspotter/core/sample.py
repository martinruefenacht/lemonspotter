"""
"""

from typing import Optional, Sequence, Callable
import logging

from core.function import Function
from core.partition import Partition
from core.parameter import Direction
from core.variable import Variable
from core.source import Source
from core.statement import ConditionStatement, FunctionStatement, ExitStatement, DeclarationAssignmentStatement, DeclarationStatement


class FunctionSample:
    """"""

    def __init__(self, function: Function, valid: bool) -> None:
        self._function: Function = function
        self._return_variable: Variable = Variable(function.return_type)

        self._arguments: Optional[Sequence[Variable]] = None
        self._evaluator: Optional[Callable[[], bool]] = None

        self._valid = valid
        # TODO expected error on invalid
        #self._partition: Partition = partition

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

    def generate_source(self, source: Source) -> Source:
        """"""

        # replace pre-existing variables in arguments
        self.arguments = [variable if source.get_variable(variable.name) is None else source.get_variable(variable.name) for variable in self.arguments]

        # add variable to source
        for variable in self.arguments:
            existing = source.get_variable(variable.name)
            if not existing:
                if variable.value:
                    source.add_at_start(DeclarationAssignmentStatement(variable))

                else:
                    source.add_at_start(DeclarationStatement(variable))

        # add function call to source
        source.add_at_start(self._generate_statement(source))

        # add outputs
        source.add_at_start(FunctionStatement.generate_print(self._return_variable))

        for parameter, argument in zip(self.function.parameters, self.arguments):
            if parameter.direction is Direction.OUT or parameter.direction is Direction.INOUT:
                source.add_at_start(FunctionStatement.generate_print(argument))

        # add check statements to call
        source.add_at_start(self._generate_return_check())

        # TODO inout/out argument checks
        # this is for in C checks
        # for parameter, variable in zip(self._function.parameters, self.arguments):
        #    if Direction(parameter.direction) is Direction.OUT:
        #        pass

        #    elif Direction(parameter.direction) is Direction.INOUT:
        #        pass

        #    else:
        #        # ignore 'in' parameters
        #        pass

        return source

    def _generate_return_check(self) -> Optional[ConditionStatement]:
        """"""

        statement = self._partition.generate_statement(self.return_variable.name)

        if statement is not None:
            # add to sub block
            statement.add_at_start(ExitStatement(self.return_variable.name))

        return statement
        # TODO expected error, valid: MPI_SUCCESS
        return None

    def _generate_statement(self, source: Source) -> FunctionStatement:
        """
        Generates a compilable expression of the function with the given arguments.
        """

        self.return_variable.name = f'return_{self.function.name}'

        if source.get_variable(self.return_variable.name) is not None:
            # todo rename output return name, we have control over this above
            raise NotImplementedError('Test if the variable already exists.')

        statement = f'{self.function.return_type.language_type} {self.return_variable.name} = {self.function.name}('

        # add arguments
        logging.debug('arguments %s', str(self.arguments))
        logging.debug('parameters %s', str(self.function.parameters))

        # fill arguments
        if self.arguments is not None:
            pairs = zip(self.arguments, self.function.parameters)  # type: ignore
            for idx, (argument, parameter) in enumerate(pairs):
                mod = ''

                pointer_diff = argument.pointer_level - parameter.pointer_level
                if pointer_diff < 0:
                    # addressof &
                    mod += '&'

                elif pointer_diff > 0:
                    # dereference *
                    raise NotImplementedError

                statement += (mod + argument.name)

                # if not last argument then add comma
                if (idx + 1) != len(self._arguments):
                    statement += ', '

        statement += ');'

        return FunctionStatement(statement, {self.return_variable.name: self.return_variable})
