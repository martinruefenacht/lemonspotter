from typing import Dict, List, Union
import logging

from core.variable import Variable

class Statement:
    def __init__(self, variables: Dict[str, Variable] = {}):
        self._variables: Dict[str, Variable] = variables
        self._statement: str = ''

    @property
    def variables(self) -> Dict[str, Variable]:
        return self._variables

    def express(self) -> str:
        return self._statement

class IncludeStatement(Statement):
    def __init__(self, header: str) -> None:
        super().__init__()

        self._statement = '#include <'+ header + '>'

class ReturnStatement(Statement):
    def __init__(self, expression: str) -> None:
        super().__init__()

        self._statement = 'return ' + expression + ';'

class DeclarationStatement(Statement):
    def __init__(self, variable: Variable):
        super().__init__()

        self._statement = variable.kind.language_type + ' ' + variable.name + ';'

    @classmethod
    def generate_declaration(cls, variable: Variable) -> 'DeclarationStatement':
        return DeclarationStatement(variable)

class AssignmentStatement(Statement):
    def __init__(self, variable: Variable):
        super().__init__()

        if variable.value:
            self._statement = variable.name + ' = ' + variable.value + ';'

        else:
            raise RuntimeError('AssignmentStatement needs Variable.value to be non-none.')

class DeclarationAssignmentStatement(Statement):
    def __init__(self, variable: Variable):
        super().__init__()

        if variable.value:
            self._statement = variable.kind.language_type + ' ' + variable.name + ' = ' + variable.value + ';'

        else:
            raise RuntimeError('DeclarationAssignmentStatement needs Variable.value to be non-none.')

    @classmethod
    def generate_assignment(cls, variable: Variable) -> 'DeclarationAssignmentStatement':
        return DeclarationAssignmentStatement(variable) 

class FunctionStatement(Statement):
    def __init__(self, statement: str, variables: Dict[str, Variable]={}):
        super().__init__(variables)

        self._statement: str = statement

    @classmethod
    def generate_print(cls, variable: Variable, capture_name: str=None) -> Union['FunctionStatement', None]:
        """
        Generate a FunctionStatement object for a given Variable.
        """

        if not variable.type.printable:
            logging.warning('%s is not printable', variable.name)
            return None

        if not capture_name:
            capture_name = variable.name

        statement = 'printf("' + capture_name + ' %' + variable.type.print_specifier + '\\n", ' + variable.name + ');'
        return FunctionStatement(statement)

class ExitStatement(Statement):
    def __init__(self, errorcode):
        super().__init__()

        self._statement: str = 'exit(' + errorcode + ');'

class BlockStatement(Statement):
    def __init__(self):
        super().__init__()

        self._front_statements: List[Statement] = []
        self._back_statements: List[Statement] = []

    def add_at_start(self, statement: Statement):
        self._front_statements.append(statement)

    def add_at_end(self, statement: Statement):
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
    def __init__(self, condition: str):
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

    @classmethod
    def generate_check(cls, variable: Variable):
        """
        """

        #if self._type.abstract_type == 'ERRORCODE':
        #    #return 'if(' + self._name + ' != MPI_SUCCESS) exit(0);'

        #    statement = ConditionStatement(self._name + ' != MPI_SUCCESS')
        #    statement.add_at_start(ExitStatement(self._name))
        #    
        #    return statement

        raise NotImplementedError


#class FunctionDefinitionStatement(BlockStatement):


