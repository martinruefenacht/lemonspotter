"""
This module defines the initiation point to finalization point generator.
"""

import logging
from typing import Set, List, Dict, Optional

from core.source import Source
from core.variable import Variable
from core.database import Database
from core.function import Function

class StartEndGenerator:
    """
    Source code generator for initiator and finalizer functions.
    """

    def __init__(self, database: Database) -> None:
        self.database = database
        self.elements_generated = 0

    def generate(self) -> Set[Source]:
        """
        Generate all possible C programs for all initiators and finalizers.
        """

        sources = set()

        # determine all start and ends
        starts = filter(lambda f: not f.needs_all and not f.needs_any,
                        self.database.functions)
        ends = filter(lambda f: not f.leads_all and not f.leads_any,
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
                path = [start, end]
                source = self.generate_source(path)
                sources.add(source)

        return sources

    def generate_source(self, path: List[Function]) -> Source:
        """
        Generate C source code for a given path between initiator and finalizer.
        """

        source = Source(''.join([func.name for func in path]))

        variables = {}
        argument_count = Variable(self.database.types_by_abstract_type['INT'], 'argument_count')
        variables[argument_count.name] = argument_count

        argument_list = Variable(self.database.types_by_abstract_type['CHAR'], 'argument_list', 2)
        variables[argument_list.name] = argument_list

        # add include directives
        ### this is essentially the template
        # TODO is it possible to abstract this?
        source.source_lines.append('#include <mpi.h>')
        source.source_lines.append('#include <stdio.h>')
        source.source_lines.append('#include <stdlib.h>')

        # TODO can we abstract this? partially with variables
        source.source_lines.append('int main(int argument_count, char **argument_list) {\n')

        for element in path:
            # TODO generate variables from parameters
            lines = self.instantiate_element(element, variables)

            for line in lines:
                source.source_lines.append(line)
                source.source_lines.append('')

        # add closing block
        source.source_lines.append('return 0;')
        source.source_lines.append('}')

        return source

    def instantiate_element(self, element: Function, variables: Dict[str, Variable]) -> List[str]:
        """
        Generate an expression which executes the given function using
        the given variables.
        """

        self.elements_generated += 1

        lines = []
        line = []

        # catch return
        return_name = 'return_' + element.name + '_' + str(self.elements_generated)
        return_expression = []
        return_expression.append(self.database.types_by_abstract_type[element.return_type].ctype)
        return_expression.append(return_name)
        return_expression.append('=')

        line.append(' '.join(return_expression))

        # add function name
        line.append(' ')
        line.append(element.name)
        line.append('(')

        # add arguments
        for parameter in element.parameters:
            # match parameter with available variable
            if parameter['name'] not in variables:
                raise NotImplementedError
                # generate variable, causes additional paths!
                # how do we handle branching points?

            variable = variables[parameter['name']]

            if variable.kind.abstract_type != parameter['abstract_type']:
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
        # TODO change to element.return_type without lookup
        return_variable = Variable(self.database.types_by_abstract_type[element.return_type], return_name)

        lines.append(return_variable.generate_print_expression())

        # return variable check
        check_expression = return_variable.generate_check_expression()
        if check_expression:
            lines.append(check_expression)

        return lines
