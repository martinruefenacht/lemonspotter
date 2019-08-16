"""
The TestGenerator is the base class for all generators.

It provides the main function definition.
"""

from core.database import Database
from core.test import Source
from core.statement import IncludeStatement, ReturnStatement, MainDefinitionStatement

class TestGenerator:
    """
    This class is the base generator class. It provides the main function
    generation.
    """

    def generate_main(self) -> Source:
        """This function generates the main function for the test."""

        source = Source()

        # add include statements
        source.add_at_start(IncludeStatement('stdio.h'))
        source.add_at_start(IncludeStatement('stdlib.h'))
        source.add_at_start(IncludeStatement('mpi.h'))

        # add main function
        block_main = MainDefinitionStatement()
        source.variables.update(block_main.variables)

        block_main.add_at_end(ReturnStatement('0'))

        source.add_at_start(block_main)

        return source
