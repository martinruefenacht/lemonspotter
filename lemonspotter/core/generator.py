import logging
from typing import Tuple, Dict

from core.source import Source
from core.variable import Variable

class Generator:
    """
    This class is the base generator class. It provides the main function
    generation.
    """

    def generate_main(self, name: str) -> Tuple[Source, Dict[str, Variable]]:
        """
        This function generates the main function for the test.
        """

        source = Source(name) 
        variables = {}

        # add include statements
        source.add_at_start('#include <mpi.h>')
        source.add_at_start('#include <stdio.h>')
        source.add_at_start('#include <stdlib.h>')

        # add main function
        source.add_at_start('int main(int argument_count, char **argument_list) {')

        # add variables
        argument_count = Variable(self.database.types_by_abstract_type['INT'],
                                  'argument_count')
        variables[argument_count.name] = argument_count

        argument_list = Variable(self.database.types_by_abstract_type['CHAR'],
                                 'argument_list',
                                 2)
        variables[argument_list.name] = argument_list

        # add closing statements
        source.add_at_end('return 0;')
        source.add_at_end('}')

        return (source, variables)
