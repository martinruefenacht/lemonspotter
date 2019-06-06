#from typing import Set, List
import logging

from lemonspotter.core import Test

class StartEndGenerator:
    """
    C source code generator for initiator and finalizer functions.
    """

#    def __init__(self, database: Database):
    def __init__(self, database):
        self.database = database

#    def generate(self) -> Set[Test]:
    def generate(self):
        """
        Generate all possible C programs for all initiators and finalizers. 
        """

        sources = set()

        # determine all start and ends
        starts = filter(lambda f: not f._needs_all and not f._needs_any,
                        self.database.function_set)
        ends   = filter(lambda f: not f._leads_all and not f._leads_any,
                        self.database.function_set)

        # for all combinations
        for start in starts:
            if start.has_failed():
                logging.warning('Skipping %s, status failed.', start.name)
                continue
            
            for end in ends:
                if end.has_failed():
                    logging.warning('Skipping %s, status failed.', end.name)
                    continue

                # generate individual test
                path = (start, end)
                source = generate_source(path)
                sources.add(source)

        return sources

#    def generate_source(self, path: List) -> Test:
    def generate_source(self, path):
        """
        Generate C source code for a given path between initiator and finalizer.
        """
        
        test = Test(''.join(path))

        # add include directives
        test.source_lines.append('#include <mpi.h>')
        test.source_lines.append('#include <stdio.h>')
        test.source_lines.append('#include <stdlib.h>')
        
        # TODO can we abstract this?
        # add main entry
        test.source_lines.append('int main(int argument_count, char **argument_list) {')

        for element in path:
            test.source_lines.append(generate_element(element))

        # add closing block
        test.source_lines.append('return 0;')
        test.source_lines.append('}')

        return test

#    def generate_element(self, element: Function) -> str:
    def generate_element(self, element):
        line = []

        # add errorcode
        errorcode = self.database.types[element['return']]['ctype']
        line.append(errorcode)

        # add function name
        line.append(element['name'])
        line.append('(')

        # add arguments
        for parameter in element.parameters:
            argument = []
            
            # add argument type
            argument.append(argtype)
            argument.append(' ')

            # add argument pointer level
            argument.append('*' * parameter.pointer)
            
            # add argument name
            argument.append(parameter['name'])

            # add comma
            if parameter is not element.parameters[-1]:
                argument.append(',')

            line.append(argument)

        line.append(')')

        return line
