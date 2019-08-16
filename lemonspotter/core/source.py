"""
This module contains the Source class.
"""

from typing import Dict, Optional
from pathlib import Path

from core.statement import Statement, BlockStatement
from core.variable import Variable


class Source:
    """
    The Source object manages all C statments and variables.
    """

    def __init__(self):
        self._variables: Dict[str, Variable] = {}

        self._front_statements = []
        self._back_statements = []

    @property
    def variables(self) -> Dict[str, Variable]:
        return self._variables

    def get_variable(self, name: str) -> Optional[Variable]:
        """This method looks up a variable by name."""

        if name in self.variables:
            return self.variables[name]

        # search sub-blocks for variables
        # todo end statements as well?
        for statement in self._front_statements:
            if issubclass(type(statement), BlockStatement):
                if name in statement.variables:
                    return statement.variables[name]

        return None

    def add_at_start(self, statement: Optional[Statement]) -> None:
        """
        Adds a generated string to the front of the source code.
        """

        if statement is None:
            return

        # todo currently only able to add to nested block
        if self._front_statements and issubclass(type(self._front_statements[-1]),
                                                 BlockStatement):
            self._front_statements[-1].add_at_start(statement)

        else:
            self._front_statements.append(statement)

            # todo how to handle this internally?
            # how do statements have access to whole global variables?
            if not issubclass(type(statement), BlockStatement):
                self._variables.update(statement.variables)

    def add_at_end(self, statement: Statement) -> None:
        """
        Adds a generated string to the back of the source code.
        """

        self._back_statements.append(statement)

        # todo we need back variables and front variables? this is ordering
        self._variables.update(statement.variables)

    def __repr__(self) -> str:
        """
        Combines the front and back lines into a single string.
        """

        code = ''

        # todo double new lines makes new lines between include statements
        # do we want that? or do we want all includes to be together?
        for statement in self._front_statements:
            code += statement.express(0) + '\n\n'

        for statement in self._back_statements:
            code += statement.express(0) + '\n\n'

        return code

    def write(self, path: Path):
        """
        Output source code into the given path.
        """

        with path.open(mode='w') as source_file:
            source_file.write(repr(self))
