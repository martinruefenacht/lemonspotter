"""
This module defines the base class Statement and all the derived classes.
"""

from typing import Dict, List, Optional, Iterable
import logging

from core.variable import Variable
from core.database import Database


class Statement:
    """
    This class is the base class for all Statements.
    """

    def __init__(self, variables: Dict[str, Variable] = None, comment: str = None) -> None:
        self._variables: Dict[str, Variable] = variables if variables else {}
        self._statement: Optional[str] = None
        self._comment: Optional[str] = comment

    @property
    def variables(self) -> Dict[str, Variable]:
        """This property provides the variables that are resident in this statement."""

        return self._variables

    def express(self, indent_level: int) -> str:
        """This method converts the Statement to a string."""

        if self._statement is None:
            raise RuntimeError('Trying to express Statement with _statement is None.')

        indentation = '\t' * indent_level

        if self._comment is not None:
            # TODO line break for long comments
            comment = f'{indentation}// {self._comment}\n'

        else:
            comment = ''

        code = f'{indentation}{self._statement}'

        return comment + code


class IncludeStatement(Statement):
    """This class represents any include statements in C."""

    def __init__(self, header: str, comment: str = None) -> None:
        super().__init__(comment=comment)

        self._statement = f'#include <{header}>'


class IncludeGroupStatement(Statement):
    """
    This class represents a group of include statements.
    """

    def __init__(self, headers: Iterable[str], comment: str = None) -> None:
        super().__init__(comment=comment)

        self._statement = '\n'.join(f'#include <{header}>' for header in headers)


class ReturnStatement(Statement):
    """This class represents any return statements in C."""

    def __init__(self, expression: str, comment: str = None) -> None:
        super().__init__(comment=comment)

        self._statement = f'return {expression};'


class DeclarationStatement(Statement):
    """This class represents any variable declaration."""

    def __init__(self, variable: Variable, comment: str = None) -> None:
        super().__init__({variable.name: variable}, comment=comment)

        self._statement = f'{variable.type.language_type} {variable.name};'

    @classmethod
    def generate_declaration(cls, variable: Variable, comment: str = None) -> 'DeclarationStatement':
        """This method generates a DeclarationStatement from a Variable."""

        return DeclarationStatement(variable, comment=comment)


class AssignmentStatement(Statement):
    """This class represents any variable assignment."""

    def __init__(self, variable: Variable, comment: str = None) -> None:
        super().__init__({variable.name: variable}, comment=comment)

        if variable.value:
            self._statement = f'{variable.name} = {variable.value};'

        else:
            raise RuntimeError('AssignmentStatement needs Variable.value to be non-none.')


class DeclarationAssignmentStatement(Statement):
    """This class represents any declaration and assignment in a single statement."""

    def __init__(self, variable: Variable, comment: str = None) -> None:
        super().__init__({variable.name: variable}, comment=comment)

        if variable.value:
            self._statement = f'{variable.type.language_type} {variable.name} = {variable.value};'

        else:
            raise RuntimeError('Variable.value required to be not be None.')

    @classmethod
    def generate_assignment(cls, variable: Variable, comment: str = None) -> 'DeclarationAssignmentStatement':
        """This method generates a DeclarationAssignmentStatement from a variable."""

        return DeclarationAssignmentStatement(variable, comment=comment)


class FunctionStatement(Statement):
    """This class represents any Function call statement."""

    def __init__(self, statement: str, variables: Dict[str, Variable] = None, comment: str = None) -> None:
        super().__init__(variables, comment=comment)

        self._statement: str = statement

    @classmethod
    def generate_print(cls, variable: Variable, comment: str = None) -> Optional['FunctionStatement']:
        """
        Generate a FunctionStatement object for a given Variable.
        """

        if not variable.type.printable:
            logging.warning('%s is not printable', variable.name)
            return None

        statement = (f'printf("{variable.name} %{variable.type.print_specifier}'
                     f'\\n", {variable.name});')

        return FunctionStatement(statement, comment=comment)


class ExitStatement(Statement):
    """This class represents any exit call."""

    def __init__(self, errorcode, comment: str = None) -> None:
        super().__init__(comment=comment)

        self._statement = f'exit({errorcode});'


class BlockStatement(Statement):
    """This class serves are a base class for block definitions."""

    def __init__(self, comment: str = None) -> None:
        super().__init__(comment=comment)

        self._front_statements: List[Statement] = []
        self._back_statements: List[Statement] = []

    def add_at_start(self, statement: Statement):
        """This method adds the statement at the start of the block."""

        self._front_statements.append(statement)
        self.variables.update(statement.variables)

    def add_at_end(self, statement: Statement):
        """This method adds the statement to the end of the block."""

        self._back_statements.append(statement)

    def express(self, indent_level: int) -> str:
        """"""

        indentation = '\t' * (indent_level-1)

        code = indentation + '{\n'

        for statement in self._front_statements:
            code += f'{statement.express(indent_level)}\n\n'

        for statement in self._back_statements:
            code += f'{statement.express(indent_level)}\n\n'

        # TODO no new line if last expression

        code += indentation + '}'

        return code


class ConditionStatement(BlockStatement):
    """This class represents if statements."""

    def __init__(self, condition: str, comment: str = None) -> None:
        super().__init__(comment = comment)

        self._condition = condition

    def express(self, indent_level: int) -> str:
        """"""

        indentation = '\t' * indent_level

        code = indentation + f'if({self._condition})\n{super().express(indent_level+1)}'

        return code


class MainDefinitionStatement(BlockStatement):
    """This class represents the main function definition."""

    def __init__(self, comment: str = None) -> None:
        super().__init__(comment=comment)

        argc = Variable(Database().type_by_abstract_type['INT'],
                        'argument_count')
        argv = Variable(Database().type_by_abstract_type['CHAR_2PTR'],
                        'argument_list')

        self._variables[argc.name] = argc
        self._variables[argv.name] = argv

        self._statement: str = f'int main(int {argc.name}, char **{argv.name})'

    def express(self, indent_level: int) -> str:
        """"""

        indentation = '\t' * indent_level

        return indentation + f'{self._statement}\n{super().express(indent_level+1)}'
