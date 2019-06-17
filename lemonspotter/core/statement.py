from typing import Dict
import os

class Statement:
    def __init__(self, variables: Dict[str, 'Variable'] = {}):
        self._variables = variables
        self._statement = ''

    @property
    def variables(self) -> Dict[str, 'Variable']:
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

#class AssignmentStatement(Statement):
#    def __init__(self, name: str):
#        super().__init__()

class FunctionStatement(Statement):
    def __init__(self, variables: Dict[str, 'Variable'], statement: str):
        super().__init__(variables)

        self._statement: str = statement

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

#class FunctionDefinitionStatement(BlockStatement):


