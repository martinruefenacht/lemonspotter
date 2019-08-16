"""
The TestGenerator is the base class for all generators.

It provides the main function definition.
"""

from core.test import Source
from core.statement import IncludeStatement, ReturnStatement, MainDefinitionStatement


class TestGenerator:
    """
    This class is the base generator class. It provides the main function
    generation.
    """

    def _generate_source_frame(self) -> Source:
        """
        This function generates the main function for the test.
        """

        source = Source()

        # add include statements
        source.add_at_start(IncludeStatement('stdio.h'))
        source.add_at_start(IncludeStatement('stdlib.h'))
        source.add_at_start(IncludeStatement('mpi.h'))
        # TODO we assume MPI here! How do we include other APIs?

        return source
