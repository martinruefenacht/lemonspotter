"""
This module defines the initiation point to finalization point generator.
"""

import logging
from typing import Set, List, Dict, Optional

from core.test import Test, Source
from core.variable import Variable
from core.database import Database
from core.function import Function
from core.generator import Generator

class StartEndGenerator(Generator):
    """
    Source code generator for initiator and finalizer functions.
    """

    def __init__(self, database: Database) -> None:
        super().__init__(database)

        self.elements_generated = 0

    def generate(self) -> Set[Test]:
        """
        Generate all possible C programs for all initiators and finalizers.
        """

        tests = set()

        # determine all start and ends
        starts = filter(lambda f: not f.needs_all and not f.needs_any,
                        self._database.functions)
        ends = filter(lambda f: not f.leads_all and not f.leads_any,
                      self._database.functions)

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
                test = self.generate_test(path)
                tests.add(test)

        return tests

    def generate_test(self, path: List[Function]) -> Test:
        """
        Generates a test object
        """

        test_name = ''.join([func.name for func in path])
        return Test(test_name, [self.generate_source(path)])

    def generate_source(self, path: List[Function]) -> Source:
        """
        Generate C source code for a given path between initiator and finalizer.
        """

        source_name = ''.join([func.name for func in path])
        source = self.generate_main(source_name)

        for function in path:
            # we have a current set of variables

            # explore all partitions for this element
            # deepcopy current source, this goes exponential
            # for each source:variables combination generate a function expression

            # TODO generate variables from parameters
            # or pass from variables

            # TODO this is temporary, we will want to do partitioning
            # TODO how to access latest block??

            # TODO how do we abstract this?
            arguments = []
            for parameter in function.parameters:
                arguments.append(source.get_variable(parameter['name']))

            # add function call
            self.elements_generated += 1
            return_name = 'return_' + function.name + '_'
            return_name += str(self.elements_generated)

            function_call = function.generate_function_statement(arguments,
                                                                 return_name,
                                                                 self._database)
            source.add_at_start(function_call)

            # add return output
            for name, variable in function_call.variables.items():
                source.add_at_start(variable.generate_print_statement())

            # add return check
            for name, variable in function_call.variables.items():
                source.add_at_start(variable.generate_check_statement())

        return source

#        # add arguments
#        for parameter in element.parameters:
#            # match parameter with available variable
#            if parameter['name'] not in variables:
#                raise NotImplementedError
#                # generate variable, causes additional paths!
#                # how do we handle branching points?
#
#            variable = variables[parameter['name']]
#
#            if variable.kind.abstract_type != parameter['abstract_type']:
#                raise ValueError('Mismatch between abstract types of parameter and variable.')
#
#            argument = []
#
#            # add argument pointer level
#            level_difference = parameter['pointer'] - variable.pointer_level
#            if level_difference > 0:
#                argument.append('&' * level_difference)
#
#            # add argument name
#            argument.append(variable.name)
#
#            # add comma
#            if parameter is not element.parameters[-1]:
#                argument.append(',')
#
#            line.append(''.join(argument))
