"""
This module defines the base class Statement and all the derived classes.
"""

from typing import Dict, List, Optional
import logging

from core.variable import Variable
from core.database import Database


class Statement:
    """
    This class is the base class for all Statements.
    """

    def __init__(self, variables: Dict[str, Variable] = None) -> None:
        self._variables: Dict[str, Variable] = variables if variables else {}
        self._statement: Optional[str] = None

    @property
    def variables(self) -> Dict[str, Variable]:
        """This property provides the variables that are resident in this statement."""

        return self._variables

    def express(self) -> str:
        """This method converts the Statement to a string."""

        if self._statement is None:
            raise RuntimeError('Trying to express Statement with _statement is None.')

        return self._statement


class IncludeStatement(Statement):
    """This class represents any include statements in C."""

    def __init__(self, header: str) -> None:
        super().__init__()

        self._statement = '#include <' + header + '>'


class ReturnStatement(Statement):
    """This class represents any return statements in C."""

    def __init__(self, expression: str) -> None:
        super().__init__()

        self._statement = 'return ' + expression + ';'


class DeclarationStatement(Statement):
    """This class represents any variable declaration."""

    def __init__(self, variable: Variable) -> None:
        super().__init__({variable.name: variable})

        self._statement = variable.type.language_type + ' ' + variable.name + ';'

    @classmethod
    def generate_declaration(cls, variable: Variable) -> 'DeclarationStatement':
        """This method generates a DeclarationStatement from a Variable."""

        return DeclarationStatement(variable)


class AssignmentStatement(Statement):
    """This class represents any variable assignment."""

    def __init__(self, variable: Variable) -> None:
        super().__init__({variable.name: variable})

        if variable.value:
            self._statement = variable.name + ' = ' + variable.value + ';'

        else:
            raise RuntimeError('AssignmentStatement needs Variable.value to be non-none.')


class DeclarationAssignmentStatement(Statement):
    """This class represents any declaration and assignment in a single statement."""

    def __init__(self, variable: Variable) -> None:
        super().__init__({variable.name: variable})

        if variable.value:
            self._statement = f'{variable.type.language_type} {variable.name} = {variable.value};'

        else:
            raise RuntimeError('Variable.value required to be not be None.')

    @classmethod
    def generate_assignment(cls, variable: Variable) -> 'DeclarationAssignmentStatement':
        """This method generates a DeclarationAssignmentStatement from a variable."""

        return DeclarationAssignmentStatement(variable)


class FunctionStatement(Statement):
    """This class represents any Function call statement."""

    def __init__(self, statement: str, variables: Dict[str, Variable] = None) -> None:
        super().__init__(variables)

        self._statement: str = statement

    @classmethod
    def generate_print(cls, variable: Variable) -> Optional['FunctionStatement']:
        """
        Generate a FunctionStatement object for a given Variable.
        """

        if not variable.type.printable:
            logging.warning('%s is not printable', variable.name)
            return None

        # TODO temporarily avoid printing pointers
        if variable.pointer_level > 0:
            logging.debug('skipping print of %s, because pointer level.', variable.name)
            return None

        statement = f'printf("{variable.name} %{variable.type.print_specifier}\\n", {variable.name});'

        logging.debug(statement)
        logging.debug(str(variable.pointer_level))

        return FunctionStatement(statement)


class ExitStatement(Statement):
    """This class represents any exit call."""

    def __init__(self, errorcode) -> None:
        super().__init__()

        self._statement: str = 'exit(' + errorcode + ');'


class BlockStatement(Statement):
    """This class serves are a base class for block definitions."""

    def __init__(self) -> None:
        super().__init__()

        self._front_statements: List[Statement] = []
        self._back_statements: List[Statement] = []

    def add_at_start(self, statement: Statement):
        """This method adds the statement at the start of the block."""

        self._front_statements.append(statement)
        self.variables.update(statement.variables)

    def add_at_end(self, statement: Statement):
        """This method adds the statement to the end of the block."""

        self._back_statements.append(statement)

    def express(self) -> str:
        code = '{\n'

        for statement in self._front_statements:
            code += statement.express() + '\n'

        for statement in self._back_statements:
            code += statement.express() + '\n'

        code += '}'

        return code


class ConditionStatement(BlockStatement):
    """This class represents if statements."""

    def __init__(self, condition: str) -> None:
        super().__init__()

        self._condition = condition

    def express(self) -> str:
        code = 'if(' + self._condition + ')\n{\n'

        for statement in self._front_statements:
            code += statement.express() + '\n'

        for statement in self._back_statements:
            code += statement.express() + '\n'

        code += '}'

        return code


class MainDefinitionStatement(BlockStatement):
    """This class represents the main function definition."""

    def __init__(self, database: Database) -> None:
        super().__init__()

        argc = Variable(database.type_by_abstract_type['INT'],
                        'argument_count')
        argv = Variable(database.type_by_abstract_type['CHAR'],
                        'argument_list')
        argv.pointer_level = 2

        self._variables[argc.name] = argc
        self._variables[argv.name] = argv

        self._statement: str = 'int main(int argument_count, char **argument_list)'

    def express(self) -> str:
        """"""

        return self._statement + '\n' + super().express()
