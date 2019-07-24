"""
This module defines the initiation point to finalization point generator.
"""

import logging
from typing import Set, List, Dict, Optional, Tuple

from core.test import Test, Source
from core.variable import Variable
from core.database import Database
from core.function import Function
from core.testgenerator import TestGenerator
from core.instantiator import Instantiator
from core.statement import FunctionStatement, ConditionStatement

class StartEndGenerator(TestGenerator):
    """
    Source code generator for initiator and finalizer functions.
    """

    def __init__(self, database: Database) -> None:
        super().__init__(database)

        self.elements_generated = 0

    def generate(self, instantiator: Instantiator) -> Set[Test]:
        """
        Generate all possible C programs for all initiators and finalizers.
        """

        # determine all start functions
        starts = filter(lambda f: not f.needs_all and not f.needs_any and
                        (f.leads_any or f.leads_all),
                        self._database.functions)

        # determine all end points
        ends = filter(lambda f: not f.leads_all and not f.leads_any and
                      (f.needs_any or f.needs_all),
                      self._database.functions)

        # TODO filter for present property

        # for all combinations
        tests = set()

        for start in starts:
            logging.info('using start %s', str(start))

            for end in ends:
                logging.info('using start %s', str(start))

                # generate individual test
                path = (start, end)
                tests = tests.union(self.generate_tests(path, instantiator))

        return tests

    def generate_tests(self, path: Tuple[Function], instantiator: Instantiator) -> Set[Test]:
        """
        Using the functions selected and the given instantiator generate a test
        for each argument set extracted from instantiator.
        """

        test_base_name = ''.join([func.name for func in path])

        tests: Set[Test] = set()

        # for all arguments (N,)^path generate test

        argument_samples: Dict[str, Tuple[Tuple[Variable]]] = {}

        # TODO this is a ^len(path) process
        for function in path:
            argument_samples.update(instantiator.generate_variables(function.parameters))

        for argument_sample_name, argument_sample in argument_samples.items():
            test_name = test_base_name + '_' + argument_sample_name

            logging.debug('generating test %s ', test_name)
            tests.add(Test(test_name, self.generate_source(path, argument_sample)))

        return tests

    def generate_source(self, path: List[Function], arguments: List[List[Variable]]) -> Source:
        """
        Generate C source code for a given path between initiator and finalizer.
        """

        source = self.generate_main()

        for idx, function in enumerate(path):
            # we have a current set of variables

            # deepcopy current source, this goes exponential
            # for each source:variables combination generate a function expression

            args = arguments[idx]
            logging.debug('%s %s', str(function), str(args))

            # add function call
            self.elements_generated += 1
            return_name = 'return_' + function.name + '_'
            return_name += str(self.elements_generated)


            function_call = function.generate_function_statement(args,
                                                                 return_name,
                                                                 self._database)
            source.add_at_start(function_call)

            # add return output
            for name, variable in function_call.variables.items():
                source.add_at_start(FunctionStatement.generate_print(variable))

            # add return check
            for name, variable in function_call.variables.items():
                source.add_at_start(ConditionStatement.generate_check(variable))

        return source

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
