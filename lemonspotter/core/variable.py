"""
This module defines the Variable class.
"""

from core.type import Type
from core.statement import FunctionStatement, ConditionStatement, ExitStatement

class Variable:
    """
    This class represents any C variable for source code generation.
    """

    def __init__(self, kind: Type, name: str, pointer_level: int = 0) -> None:
        """
        This method constructs the Variable from a type, name and pointer level.
        """

        self._kind: Type = kind
        self._name: str = name
        self._pointer_level: int = pointer_level

    @property
    def kind(self) -> Type:
        return self._kind

    @property
    def name(self) -> str:
        return self._name

    @property
    def pointer_level(self) -> int:
        return self._pointer_level

    def generate_print_statement(self) -> FunctionStatement:
        """
        Generates a C printf statement for this variable.
        """

        # hard coded mapping between printf format and C type
        if self._kind.abstract_type == 'ERRORCODE':
            # this is a function call statement
            # we don't care about return variable though

            statement = 'printf("' + self._name + ' %i\\n", ' + self._name + ');'
            return FunctionStatement({}, statement) 

        raise NotImplementedError

    def generate_check_statement(self) -> ConditionStatement:
        """
        Generates a C statement to check if the variable is valid.
        """

        if self._kind.abstract_type == 'ERRORCODE':
            #return 'if(' + self._name + ' != MPI_SUCCESS) exit(0);'

            statement = ConditionStatement(self._name + ' != MPI_SUCCESS')
            statement.add_at_start(ExitStatement(self._name))
            
            return statement

        raise NotImplementedError
