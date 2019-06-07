#from typing import Set, List
import logging

from core.source import Source

class StartEndGenerator:
    """
    C source code generator for initiator and finalizer functions.
    """

#    def __init__(self, database: Database):
    def __init__(self, database):
        self.database = database

#    def generate(self) -> Set[Source]:
    def generate(self):
        """
        Generate all possible C programs for all initiators and finalizers. 
        """

        sources = set()

        # determine all start and ends
        starts = filter(lambda f: not f._needs_all and not f._needs_any,
                        self.database.functions)
        ends   = filter(lambda f: not f._leads_all and not f._leads_any,
                        self.database.functions)

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
                source = self.generate_source(path)
                sources.add(source)

        return sources

#    def generate_source(self, path: List) -> Test:
    def generate_source(self, path):
        """
        Generate C source code for a given path between initiator and finalizer.
        """
        
        source = Source(''.join([func.function_name for func in path]))

        # add include directives
        source.source_lines.append('#include <mpi.h>')
        source.source_lines.append('#include <stdio.h>')
        source.source_lines.append('#include <stdlib.h>')
        
        # TODO can we abstract this?
        # add main entry
        source.source_lines.append('int main(int argument_count, char **argument_list) {')

        for element in path:
            source.source_lines.append(self.generate_element(element))

        # add closing block
        source.source_lines.append('return 0;')
        source.source_lines.append('}')

        return source

#    def generate_element(self, element: Function) -> str:
    def generate_element(self, element):
        line = []

        # add errorcode
        errorcode = self.database.types_by_abstract_type[element.return_type].ctype
        #print(errorcode)
        line.append(errorcode)

        # add function name
        line.append(element.function_name)
        line.append('(')

        # add arguments
        for parameter in element.parameters:
            argument = []
            
            print(self.database.types_by_abstract_type[parameter['abstract_type']].classification)

            # add argument type
            argument.append(self.database.types_by_abstract_type[parameter['abstract_type']].ctype)
            argument.append(' ')

            # add argument pointer level
            argument.append('*' * parameter['pointer'])
            
            # add argument name
            argument.append(parameter['name'])

            # add comma
            if parameter is not element.parameters[-1]:
                argument.append(',')

            line.append(argument)

        line.append(')')

        #print(line)

        return line
