#from typing import Set, List
import logging

from core.source import Source
from core.variable import Variable

class StartEndGenerator:
    """
    C source code generator for initiator and finalizer functions.
    """

#    def __init__(self, database: Database):
    def __init__(self, database):
        self.database = database
        self.elements_generated = 0

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
        
        source = Source(''.join([func.name for func in path]))

        variables = {}
        v1 = Variable(self.database.types_by_abstract_type['INT'], 'argument_count')
        variables[v1.name] = v1

        v2 = Variable(self.database.types_by_abstract_type['CHAR'], 'argument_list', 2)
        variables[v2.name] = v2

        # add include directives
        ### this is essentially the template
        # TODO is it possible to abstract this?
        source.source_lines.append('#include <mpi.h>')
        source.source_lines.append('#include <stdio.h>')
        source.source_lines.append('#include <stdlib.h>')
        
        # TODO can we abstract this? partially with variables
        # add main entry
        source.source_lines.append('int main(int argument_count, char **argument_list) {\n')

        for element in path:
            lines = self.instantiate_element(element, variables)

            for line in lines:
                source.source_lines.append(line)
                source.source_lines.append('')

        # add closing block
        source.source_lines.append('return 0;')
        source.source_lines.append('}')

        return source

#    def generate_element(self, element: Function) -> str:
    def instantiate_element(self, element, variables):
        self.elements_generated += 1

        lines = []
        line = []

        # catch return
        #line.append(element.return_type.ctype + ' = ');
        return_name = 'ret' + str(self.elements_generated)
        line.append(self.database.types_by_abstract_type[element.return_type]._ctype + ' ' + return_name + ' = ');

        # add function name
        line.append(element.name)
        line.append('(')

        # add arguments
        for parameter in element.parameters:
            # match parameter with available variable
            variable = variables[parameter['name']]

            if variable.typeof.abstract_type != parameter['abstract_type']:
                raise ValueError('Mismatch between abstract types of parameter and variable.')

            argument = []
            
            # add argument pointer level
            level_difference = parameter['pointer'] - variable.pointer_level
            if level_difference > 0:
                argument.append('&' * level_difference)
            
            # add argument name
            argument.append(variable.name)

            # add comma
            if parameter is not element.parameters[-1]:
                argument.append(',')

            line.append(''.join(argument))

        line.append(');')

        lines.append(''.join(line))

        # return variable output
        return_variable = Variable(self.database.types_by_abstract_type[element.return_type], return_name) 
    
        lines.append(self.generate_print_variable(return_variable))

        return lines

    def generate_print_variable(self, variable):
        if variable.typeof._ctype == 'int':
            return 'printf("%i\\n", ' + variable.name + ');'

        else:
            raise ValueError('Variable has type ' + variable.typeof.abstract_type + ' is     not known to print.')
