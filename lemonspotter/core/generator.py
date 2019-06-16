import logging
from typing import Dict

from core.database import Database
from core.source import Source
from core.variable import Variable
from core.statement import IncludeStatement, ReturnStatement, BlockStatement
from core.function import MainFunctionStatement

class Generator:
    """
    This class is the base generator class. It provides the main function
    generation.
    """

    def __init__(self, database: Database) -> None:
        self._database = database

    def generate_main(self, name: str) -> Source:
        """
        This function generates the main function for the test.
        """

        source = Source(name) 

        # add include statements
        source.add_at_start(IncludeStatement('stdio.h'))
        source.add_at_start(IncludeStatement('stdlib.h'))
        source.add_at_start(IncludeStatement('mpi.h'))

        # add main function
        source.add_at_start(MainFunctionStatement(self._database))
        
        block_main = BlockStatement()
        block_main.add_at_end(ReturnStatement('0'))

        source.add_at_start(block_main)

        return source
