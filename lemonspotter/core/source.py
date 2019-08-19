"""
This module contains the Source class.
"""

from typing import Optional
from pathlib import Path

from core.statement import Statement, SourceStatement
from core.variable import Variable


class Source:
    """
    The Source object manages all C statments and variables.
    """

    def __init__(self) -> None:
        self._block_statement = SourceStatement()

    def has_variable(self, name: str) -> bool:
        """"""

        return self._block_statement.has_variable(name)

    def get_variable(self, name: str) -> Optional[Variable]:
        """This method looks up a variable by name."""

        return self._block_statement.get_variable(name)

    def add_at_start(self, statement: Optional[Statement]) -> None:
        """
        Adds a generated string to the front of the source code.
        """

        if statement is not None:
            self._block_statement.add_at_start(statement)

    def add_at_end(self, statement: Statement) -> None:
        """
        Adds a generated string to the back of the source code.
        """

        self._block_statement.add_at_end(statement)

    def __repr__(self) -> str:
        """
        Combines the front and back lines into a single string.
        """

        return self._block_statement.express(0)

    def write(self, path: Path):
        """
        Output source code into the given path.
        """

        with path.open(mode='w') as source_file:
            source_file.write(repr(self))
