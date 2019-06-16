from typing import Union, Dict

from core.statement import Statement, BlockStatement
from core.variable import Variable

class Source:
    def __init__(self, name: str):
        self._name: str = name

        self._variables: Dict[str, Variable] = {}

        self._front_statements = []
        self._back_statements = []

    @property
    def variables(self) -> Dict[str, Variable]:
        return self._variables

    def add_at_start(self, statement: Statement) -> None:
        """
        Adds a generated string to the fron of the source code.
        """

        self._front_statements.append(statement)

        if not issubclass(type(statement), BlockStatement):
            self._variables.update(statement.variables)

    def add_at_end(self, statement: Statement) -> None:
        """
        Adds a generated string to the back of the source code.
        """

        self._back_statements.append(statement)
        self._variables.update(statement.variables)

    def get_source(self) -> str:
        """
        Combines the front and back lines into a single string. 
        """

        code = ''
        
        for statement in self._front_statements:
            code += statement.express() + '\n'

        for statement in self._back_statements:
            code += statement.express() + '\n'

        return code
