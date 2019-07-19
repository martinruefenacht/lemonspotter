"""
This module defines the Variable class.
"""

from typing import Union
import logging

from core.type import Type
from core.statement import FunctionStatement, ConditionStatement, ExitStatement, DeclarationStatement, DeclarationAssignmentStatement

class Variable:
    """
    This class represents any C variable for source code generation.
    """

    def __init__(self, kind: Type, name: str, value: str=None, pointer_level: int = 0) -> None:
        """
        This method constructs the Variable from a type, name and pointer level.
        """

        self._type: Type = kind
        self._name: str = name
        self._value: str = value
        self._pointer_level: int = pointer_level
        
    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self._name

    @property
    def kind(self) -> Type:
        return self._type

    @property
    def type(self) -> Type:
        return self._type

    @property
    def name(self) -> str:
        return self._name

    @property
    def pointer_level(self) -> int:
        return self._pointer_level

    def generate_print_statement(self, capture_name=None) -> Union[FunctionStatement, None]:
        """
        Generates a C printf statement for this variable.
        """

        if not self.type.printable:
            logging.warning('%s is not printable', self.name)
            return

        if not capture_name:
            capture_name = self.name

        statement = 'printf("' + capture_name + ' %' + self.type.print_specifier + '\\n", ' + self.name + ');'
        return FunctionStatement({}, statement)

    def generate_check_statement(self) -> ConditionStatement:
        """
        Generates a C statement to check if the variable is valid.
        """
        
        # TODO custom check statements for types!

        if self._type.abstract_type == 'ERRORCODE':
            #return 'if(' + self._name + ' != MPI_SUCCESS) exit(0);'

            statement = ConditionStatement(self._name + ' != MPI_SUCCESS')
            statement.add_at_start(ExitStatement(self._name))
            
            return statement

        raise NotImplementedError

    def generate_declaration_statement(self) -> Union[DeclarationStatement, DeclarationAssignmentStatement]:
        if self._value:
            return DeclarationAssignmentStatement(self, self._value)

        else:
            return DeclarationStatement(self)
