"""
The TestGenerator is the base class for all generators.

It provides the main function definition.
"""

import logging
from typing import Dict

from core.database import Database
from core.test import Source
from core.variable import Variable
from core.statement import IncludeStatement, ReturnStatement
from core.function import MainDefinitionStatement

class TestGenerator:
    """
    This class is the base generator class. It provides the main function
    generation.
    """

    def __init__(self, database: Database) -> None:
        self._database = database

    def generate_main(self) -> Source:
        """
        This function generates the main function for the test.
        """

        source = Source()
        variables = {}

        # add include statements
        source.add_at_start(IncludeStatement('stdio.h'))
        source.add_at_start(IncludeStatement('stdlib.h'))
        source.add_at_start(IncludeStatement('mpi.h'))

        # add main function
        block_main = MainDefinitionStatement(self._database)

        block_main.add_at_end(ReturnStatement('0'))
        #block_main.add_at_end(ReturnStatement(block_main.variables['argument_count'].name))

        source.add_at_start(block_main)

        return source
