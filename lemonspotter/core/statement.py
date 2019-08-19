"""
This module defines the base class Statement and all the derived classes.
"""

from typing import Dict, List, Optional
import logging
from itertools import tee, chain

from core.variable import Variable
from core.database import Database


class Statement:
    """
    This class is the base class for all Statements.
    """

    indent: str = '\t'
    max_line_length: int = 80

    def __init__(self, variables: Dict[str, Variable] = None, comment: str = None) -> None:
        self._variables: Dict[str, Variable] = variables if variables else {}
        self._statement: Optional[str] = None
        self._comment: str = comment.strip() if comment else ''

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, comment: str) -> None:
        self._comment = comment.strip() if comment else ''

    def get_variable(self, name: str) -> Optional[Variable]:
        """"""

        return self._variables.get(name, None)

    def has_variable(self, name: str) -> bool:
        """"""

        return name in self._variables

    def express(self, indent_level: int) -> str:
        """This method converts the Statement to a string."""

        if self._statement is None:
            raise RuntimeError('Trying to express Statement with _statement is None.')

        indentation = self.indent * indent_level
        assert len(indentation) < self.max_line_length

        if self._comment:
            comment = f'{indentation}// {self._comment}\n'

            if len(comment) < self.max_line_length:
                # single line comment
                final_comment = comment

            else:
                final_comment = ''

                # multi line comment using // instead of /* */
                overrun = len(comment) - self.max_line_length

                while overrun > 0:
                    # find breakable space character
                    index = comment.rfind(' ', 0, self.max_line_length)
                    final_comment += comment[:index] + '\n'

                    # separate comment lines
                    comment = f'{indentation}// {comment[index:].strip()}'
                    overrun = len(comment) - self.max_line_length

                final_comment += comment + '\n'

        else:
            final_comment = ''

        full_statement = f'{final_comment}{indentation}{self._statement}'

        return full_statement


class BlockStatement(Statement):
    """This class serves are a base class for block definitions."""

    def __init__(self, comment: str = None) -> None:
        super().__init__(comment=comment)

        self._front_statements: List[Statement] = []
        self._back_statements: List[Statement] = []

    def get_variable(self, name: str) -> Optional[Variable]:
        if name in self._variables:
            return self._variables[name]

        else:
            for statement in (self._front_statements + self._back_statements):
                var = statement.get_variable(name)
                if var is not None:
                    return var

        return None

    def has_variable(self, name: str) -> bool:
        """"""

        internal = name in self._variables

        if internal:
            return internal

        else:
            for statement in (self._front_statements + self._back_statements):
                if statement.has_variable(name):
                    return True

        return False

    def add_at_start(self, statement: Optional[Statement]) -> None:
        """This method adds the statement at the start of the block."""

        if statement is None:
            return

        self._front_statements.append(statement)

    def add_at_end(self, statement: Optional[Statement]):
        """This method adds the statement to the end of the block."""

        if statement is None:
            return

        self._back_statements.append(statement)

    def express(self, indent_level: int) -> str:
        """"""

        indentation = self.indent * (indent_level-1)

        return f'{indentation}{{\n{self.express_statements(indent_level)}{indentation}}}'

    def express_statements(self, indent_level: int) -> str:
        code = ''

        if self._front_statements or self._back_statements:
            # TODO clean this method up

            def prepair(iterable):
                prevs, items = tee(iterable)
                prevs = chain([None], prevs)
                return zip(prevs, items)

            def concat_statements(statements):
                exp = []

                for previous, statement in prepair(statements):
                    c = ''
                    if previous is not None:
                        if not isinstance(previous, type(statement)):
                            c += '\n'

                        elif (isinstance(previous, FunctionStatement) and
                              isinstance(statement, FunctionStatement) and
                              previous.function != statement.function):
                            c += '\n'

                    exp.append(f'{c}{statement.express(indent_level)}')

                return '\n'.join(exp)

            # unrolled last element to avoid unwanted new line
            statements = self._front_statements + self._back_statements

            if len(statements) > 1:
                code += concat_statements(statements[:-1])
                code += '\n'

                # new line between different statement types
                if not isinstance(statements[-1], type(statements[-2])):
                    code += '\n'

            # express last statement
            code += f'{statements[-1].express(indent_level)}\n'

        return code


class SourceStatement(BlockStatement):
    """
    This BlockStatement subclass serves the Source expression as a simplification to the
    BlockStatement express method, to reduce the branching.
    """

    def express(self, indent_level: int) -> str:
        return self.express_statements(indent_level)


class IncludeStatement(Statement):
    """This class represents any include statements in C."""

    def __init__(self, header: str, comment: str = None) -> None:
        super().__init__(comment=comment)

        self._statement = f'#include <{header}>'


class CommentStatement(Statement):
    """"""

    def __init__(self, comment: str) -> None:
        super().__init__()

        self._statement = f'// {comment}'


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
    def generate_declaration(cls,
                             variable: Variable,
                             comment: str = None) -> 'DeclarationStatement':
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
    def generate_assignment(cls,
                            variable: Variable,
                            comment: str = None) -> 'DeclarationAssignmentStatement':
        """This method generates a DeclarationAssignmentStatement from a variable."""

        return DeclarationAssignmentStatement(variable, comment=comment)


class FunctionStatement(Statement):
    """This class represents any Function call statement."""

    def __init__(self,
                 function: Optional[str],
                 statement: str,
                 variables: Dict[str, Variable] = None,
                 comment: str = None) -> None:
        super().__init__(variables, comment=comment)

        self._function = function
        self._statement: str = statement

    @property
    def function(self) -> Optional[str]:
        return self._function

    @classmethod
    def generate_print(cls,
                       variable: Variable,
                       comment: str = None) -> Optional['FunctionStatement']:
        """
        Generate a FunctionStatement object for a given Variable.
        """

        if not variable.type.printable:
            logging.info('%s is not printable, no Statement will be emitted.', variable.name)
            return None

        statement = (f'printf("{variable.name} %{variable.type.print_specifier}'
                     f'\\n", {variable.name});')

        return FunctionStatement('printf', statement, comment=comment)


class ExitStatement(Statement):
    """This class represents any exit call."""

    def __init__(self, errorcode, comment: str = None) -> None:
        super().__init__(comment=comment)

        self._statement = f'exit({errorcode});'


class ConditionStatement(BlockStatement):
    """This class represents if statements."""

    def __init__(self, condition: str, comment: str = None) -> None:
        super().__init__(comment=comment)

        self._condition = condition

    def express(self, indent_level: int) -> str:
        """"""

        indentation = self.indent * indent_level

        code = indentation + f'if({self._condition})\n{super().express(indent_level+1)}'

        return code


class MainDefinitionStatement(BlockStatement):
    """This class represents the main function definition."""

    def __init__(self, comment: str = None) -> None:
        super().__init__(comment=comment)

        argc = Variable(Database().get_type('INT'),
                        'argument_count')
        argv = Variable(Database().get_type('CHAR_2PTR'),
                        'argument_list')

        self._variables[argc.name] = argc
        self._variables[argv.name] = argv

        self._statement: str = f'int main(int {argc.name}, char **{argv.name})'

    def express(self, indent_level: int) -> str:
        """"""

        indentation = self.indent * indent_level

        return indentation + f'{self._statement}\n{super().express(indent_level+1)}'
