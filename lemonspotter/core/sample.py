"""
"""

from typing import Optional, Sequence, Callable, Iterable
import logging

from lemonspotter.core.function import Function
from lemonspotter.core.parameter import Direction
from lemonspotter.core.variable import Variable
from lemonspotter.core.statement import (ConditionStatement,
                                         FunctionStatement,
                                         ExitStatement,
                                         DeclarationAssignmentStatement,
                                         DeclarationStatement,
                                         BlockStatement)


class FunctionSample:
    """"""

    def __init__(self,
                 function: Function,
                 valid: bool,
                 variables: Iterable[Variable] = set(),
                 arguments: Sequence[Variable] = [],
                 evaluator: Optional[Callable[[], bool]] = None,
                 ) -> None:
        self._function = function
        self._valid = valid
        self._variables = variables
        self._arguments = arguments
        self._evaluator = evaluator

        self._return_variable: Variable = Variable(function.return_type)

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

        return self._arguments

    @arguments.setter
    def arguments(self, arguments: Sequence[Variable]) -> None:
        """"""

        if arguments is None:
            raise Exception('Arguments given to Sample are None.')

        self._arguments = arguments

    @property
    def variables(self) -> Iterable[Variable]:
        """"""

        return self._variables

    @variables.setter
    def variables(self, variables: Iterable[Variable]) -> None:
        """"""

        if variables is None:
            raise Exception('Variables given to Sample is None.')

        self._variables = variables

    @property
    def evaluator(self) -> Callable[[], bool]:
        """"""

        if self._evaluator is None:
            raise Exception('Evaluator is None. Needs to be assigned.')

        return self._evaluator

    @evaluator.setter
    def evaluator(self, evaluator: Callable[[], bool]) -> None:
        """"""

        if evaluator is None:
            raise Exception('Evaluator given to Sample is None.') 

        self._evaluator = evaluator

    def generate_source(self, source: BlockStatement, comment: str = None) -> None:
        """"""

        # assign predefined arguments and check for collisions
        def check_argument(arg):
            if arg.predefined:
                predef = source.get_variable(arg.value)

                if predef is None:
                    raise RuntimeError('Predefined variable not present in source.')

                if predef.type is arg.type:
                    return predef

                else:
                    # try referencing
                    if predef.type.referencable:
                        # create variable
                        var = Variable(predef.type.reference(),
                                       f'{predef.name}_ref',
                                       f'&{predef.name}')

                        return var

            elif source.get_variable(arg.name) is not None:
                raise RuntimeError('Name collision found between argument and variable.')

            else:
                return arg

        self.arguments = [check_argument(argument) for argument in self.arguments]

        # add arguments to source
        for variable in self.arguments:
            existing = source.get_variable(variable.name)
            if not existing:
                if variable.value:
                    source.add_at_start(DeclarationAssignmentStatement(variable))

                else:
                    source.add_at_start(DeclarationStatement(variable))

        # add function call to source
        source.add_at_start(self._generate_statement(source, comment))

        # add outputs
        source.add_at_start(FunctionStatement.generate_print(self._return_variable))

        for parameter, argument in zip(self.function.parameters, self.arguments):  # type: ignore
            if parameter.direction is Direction.OUT or parameter.direction is Direction.INOUT:
                source.add_at_start(FunctionStatement.generate_print(argument))

        # add check statements to call
        source.add_at_start(self._generate_return_check())

        # note, we check out argument validity in LemonSpotter level
        # note, should we even do a return check?

    def _generate_return_check(self) -> Optional[ConditionStatement]:
        """"""

        # TODO let partition generate condition statement
        # statement = self._partition.generate_statement(self.return_variable.name)
        # function sample checks for self._valid, don't assume MPI_SUCCESS

        if self._valid:
            source = f'{self._return_variable.name} != MPI_SUCCESS'
        else:
            source = f'{self._return_variable.name} == MPI_SUCCESS'

        statement = ConditionStatement(source)

        if statement is not None:
            # add to sub block
            statement.add_at_start(ExitStatement(self.return_variable.name))

        return statement

    def _generate_statement(self,
                            source: BlockStatement,
                            comment: str = None) -> FunctionStatement:
        """
        Generates a compilable expression of the function with the given arguments.
        """

        self.return_variable.name = f'return_{self.function.name}'

        if source.get_variable(self.return_variable.name) is not None:
            # todo rename output return name, we have control over this above
            raise NotImplementedError('Test if the variable already exists.')

        statement = (f'{self.function.return_type.language_type} {self.return_variable.name}'
                     f' = {self.function.name}(')

        # add arguments
        logging.debug('arguments %s', str(self.arguments))
        logging.debug('parameters %s', str(self.function.parameters))

        # fill arguments
        if self.arguments is not None:
            pairs = zip(self.arguments, self.function.parameters)  # type: ignore
            for idx, (argument, parameter) in enumerate(pairs):
                mod = ''

#                pointer_diff = argument.pointer_level - parameter.pointer_level
#                if pointer_diff < 0:
#                    # addressof &
#                    mod += '&'
#
#                elif pointer_diff > 0:
#                    # dereference *
#                    raise NotImplementedError

                statement += (mod + argument.name)

                # if not last argument then add comma
                if (idx + 1) != len(self._arguments):
                    statement += ', '

        statement += ');'

        return FunctionStatement(self._function.name,
                                 statement,
                                 {self.return_variable.name: self.return_variable},
                                 comment)
