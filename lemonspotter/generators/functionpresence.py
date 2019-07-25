"""
This module defines the function presence test generator.

Tests whether a specific function is linkable. No execution is required only
building success or fail.
"""

import logging
from typing import Set

from core.database import Database
from core.test import Test, TestType
from core.function import Function
from core.variable import Variable
from core.testgenerator import TestGenerator
from core.statement import DeclarationStatement


class FunctionPresenceGenerator(TestGenerator):
    """
    """

    def __init__(self, database: Database) -> None:
        super().__init__(database)

    def generate(self) -> Set[Test]:
        """
        Generates all presence test objects for all functions in the database.
        """

        tests = set()

        # find all functions which have not been tested
        functions = filter(lambda f: not f.properties.get('presence_tested', False),
                           self._database.functions)

        # for all applicable functions
        for func in functions:
            test = self.generate_test(func)

            logging.debug(('function test generated for %s:\n' + repr(test.source)), func.name)

            tests.add(test)

        return tests

    def generate_test(self, function: Function) -> Test:
        """
        Generates a Test object containing a valid main block and a function call without
        check or print statements.
        """

        logging.info('generating test for %s', function.name)

        source = self.generate_main()

        # generate default function arguments
        arguments = []

        for parameter in function.parameters:  # type: ignore
            if parameter.name not in source.variables:
                # TODO doesn't take into account pointer_level
                variable = Variable(parameter.type, parameter.name)

                source.variables[variable.name] = variable

                # only requires valid types, not correct code for presence testing
                source.add_at_start(DeclarationStatement.generate_declaration(variable))

            else:
                variable = source.variables[parameter.name]

            arguments.append(variable)

        # generate function call statement
        return_name = 'return_' + function.name
        function_call = function.generate_function_statement(tuple(arguments), return_name)

        source.add_at_start(function_call)

        # create Test and assign build success/fail closures
        test = Test('function_presence_' + function.name, source, test_type=TestType.BUILD_ONLY)

        def build_fail():
            function.properties['presence_tested'] = True
            function.properties['present'] = False
        test.build_fail_function = build_fail

        def build_success():
            function.properties['presence_tested'] = True
            function.properties['present'] = True
        test.build_success_function = build_success

        return test
