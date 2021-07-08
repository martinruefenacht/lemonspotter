"""
Defines the FunctionSample class.
"""

from typing import Optional, Callable, Mapping, MutableMapping
import logging
from itertools import chain

from lemonspotter.core.function import Function
from lemonspotter.core.parameter import Parameter
from lemonspotter.core.argument import Argument
from lemonspotter.core.parameter import Direction
from lemonspotter.core.variable import Variable
from lemonspotter.core.statement import (ConditionStatement,
                                         FunctionStatement,
                                         ExitStatement,
                                         DeclarationAssignmentStatement,
                                         DeclarationStatement,
                                         BlockStatement)


class FunctionSample:
    """
    Container for a function and arguments.
    """

    def __init__(self,
                 function: Function,
                 valid: bool,
                 arguments: Optional[MutableMapping[str, Argument]] = None,
                 evaluator: Optional[Callable[[], bool]] = None,
                 ) -> None:
        self._function = function
        self._valid = valid
        self._arguments: MutableMapping[str, Argument] = arguments if arguments else {}
        self._evaluator = evaluator

        # generate out variables, return, and out parameters
        self._return_variable = Variable(function.return_type,
                                         'return_' + function.name)
        self._generate_out_arguments()

    @property
    def function(self) -> Function:
        """
        Retrieve the Function object which this FunctionSample is a sample of.
        """

        return self._function

    @property
    def return_variable(self) -> Variable:
        """
        Retrieve the Variable instance which is the return variable of this
        FunctionSample instance.
        """

        return self._return_variable

    @property
    def arguments(self) -> Mapping[str, Argument]:
        """
        Gets the arguments from this FunctionSample.
        """

        return self._arguments

    @property
    def evaluator(self) -> Callable[[], bool]:
        """
        Gets the evaluator function for this FunctionSample.
        """

        if self._evaluator is None:
            raise RuntimeError('Evaluator is None. Needs to be assigned.')

        return self._evaluator

    @evaluator.setter
    def evaluator(self, evaluator: Callable[[], bool]) -> None:
        """
        Sets the evaluator function for this FunctionSample.
        """

        if evaluator is None:
            raise RuntimeError('Evaluator given to Sample is None.')

        self._evaluator = evaluator

    def generate_source(self, source: BlockStatement, comment: str = None) -> None:
        """
        Expresses the FunctionSample as a FunctionStatement and adds it to the given
        Source.
        """

        # add arguments to source
        logging.debug('Arguments: %s', self.arguments)
        logging.debug('Source variables %s', source._variables)
        for parameter in self.function.parameters:
            # fetch argument
            argument = self.arguments[parameter.name]

            # add dependent variables to source
            # TODO
            # same procedure as below?

            # add argument variable to source
            if argument.variable.predefined:
                # argument.variable.value has to match a source variable
                # get variable from source
                source_variable = source.get_variable(argument.variable.name)
                if source_variable is None:
                    raise RuntimeError('Predefined argument %s not found in source %s.',
                                       argument.variable.name,
                                       source._variables)

                if source_variable is argument.variable.type:
                    # variable found is identical to required
                    pass

                else:
                    if source_variable.type.referencable:
                        transition_variable = Variable(source_variable.type.reference(),
                                                       f'{source_variable.name}_ref',
                                                       f'&{source_variable.name}')
                        source.add_at_start(DeclarationAssignmentStatement(transition_variable))
                        # this variable needs to be referenced in the function statement!

                        self._arguments[parameter.name] = Argument(transition_variable)

                    else:
                        raise NotImplementedError('variable of predefined found, but not same '
                                                  'type.')

            elif not source.get_variable(argument.variable.name):
                if argument.variable.value:
                    source.add_at_start(DeclarationAssignmentStatement(argument.variable))

                else:
                    source.add_at_start(DeclarationStatement(argument.variable))

        # add function call to source
        source.add_at_start(self._generate_statement(source, comment))

        # add outputs
        source.add_at_start(FunctionStatement.generate_print(self._return_variable))

        for parameter in chain(self.function.out_parameters, self.function.inout_parameters):
            source.add_at_start(FunctionStatement.generate_print(
                self.arguments[parameter.name].variable))

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

        if source.get_variable(self.return_variable.name) is not None:
            # todo rename output return name, we have control over this above
            raise NotImplementedError('Return variable already exists!.')
        # TODO need to check out arguments as well

        statement = []
        statement.append((f'{self.function.return_type.language_type} '
                          f'{self.return_variable.name} '
                          f'= {self.function.name}('))

        # fill arguments
        if self.function.has_parameters:
            for idx, parameter in enumerate(self.function.parameters):
                # get argument for parameter
                argument = self.arguments[parameter.name]

                statement.append(argument.variable.name)

                # if not last argument then add comma
                if (idx + 1) != len(self.function.parameters):
                    statement.append(', ')

        statement.append(');')

        logging.debug('function statement %s', ''.join(statement))

        return FunctionStatement(self._function.name,
                                 ''.join(statement),
                                 {self.return_variable.name: self.return_variable},
                                 comment)

    def _generate_out_arguments(self) -> None:
        """
        Generates appropriate out variables for the out parameters.
        """

        logging.debug('generating out arguments for %s', self.function.name)
        logging.debug('out parameters %s', self.function.out_parameters)

        for parameter in self.function.out_parameters:
            logging.debug('generating out argument for parameter %s', parameter.name)

            # generate out variable and its dependents
            value = None

            # TODO this doesn't really capture it, some types are dereferencable,
            # but need to be passed in as is
            if parameter.type.abstract_type == 'STRING':
                value = f'malloc({parameter.length} * sizeof(char))'

            elif parameter.type.dereferencable:
                value = f'malloc(sizeof({parameter.type.dereference().language_type}))'

            self._arguments[parameter.name] = Argument(Variable(
                parameter.type,
                parameter.name + '_out',
                value))
