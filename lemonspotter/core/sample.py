"""
"""

from typing import Optional, Sequence, Callable, Iterable 
import logging

from core.function import Function
from core.partition import Partition
from core.variable import Variable
from core.source import Source
from core.statement import ConditionStatement, FunctionStatement, ExitStatement, DeclarationAssignmentStatement, DeclarationStatement


class FunctionSample:
    """"""

    def __init__(self, function: Function, partition: Partition) -> None:
        self._function: Function = function
        self._return_variable: Variable = Variable(function.return_type)

        self._arguments: Optional[Sequence[Variable]] = None
        self._evaluator: Optional[Callable[[], bool]] = None

        # TODO this has to be removed!
        self._partition: Partition = partition

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

        # add variable to source
        for variable in self.arguments:
            # TODO this is where main(argc, argv) comes in
            if variable.name not in source.variables:
                if variable.value:
                    source.add_at_start(DeclarationAssignmentStatement(variable))
                
                else:
                    source.add_at_start(DeclarationStatement(variable))

        # add function call to source
        source.add_at_start(self._generate_statement(source))

        # add print statement to call
        source.add_at_start(FunctionStatement.generate_print(self._return_variable))

        # add check statements to call
        source.add_at_start(self._generate_return_check())
        
        # TODO inout/out argument checks
        # may not be possible... provided is a set of 4 not a single one
        # for MPI_Init_thread
        #for statement in self._generate_argument_checks():
        #    source.add_at_start(statement)

        return source

    def _generate_return_check(self) -> ConditionStatement:
        """"""

        # invert operand
        if self._partition.return_operand == 'equal':
            op = '!='
        else:
            raise NotImplementedError('Other return operands not implemented. operand is "' +
                                      str(self._partition.return_operand) + '" for function ' +
                                      self._function.name)

        statement = ConditionStatement(' '.join([self._return_variable.name, 
                                                op,
                                                self._partition.return_symbol]))
        statement.add_at_start(ExitStatement(self._return_variable.name))

        return statement

    #def _generate_argument_checks(self) -> Iterable[ConditionStatement]:
    # check is out arguments are in specification valid

    def _generate_statement(self, source: Source) -> FunctionStatement:
        """
        Generates a compilable expression of the function with the given arguments.
        """

        self._return_variable.name = 'return_' + self._function.name

        if self._return_variable.name in source.variables:
            # todo rename output return name, we have control over this above
            raise NotImplementedError('Test if the variable already exists.')

        statement = ''
        statement += self.function.return_type.language_type + ' ' + self._return_variable.name
        statement += ' = '
        statement += self.function.name + '('

        # add arguments
        logging.debug('arguments %s', str(self._arguments))
        logging.debug('parameters %s', str(self.function.parameters))

        # fill arguments
        if self._arguments is not None:
            pairs = zip(self._arguments, self.function.parameters)  # type: ignore
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

        return FunctionStatement(statement, {self._return_variable.name: self._return_variable})
