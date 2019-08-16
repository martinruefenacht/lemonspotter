"""
This module defines the function presence test generator.

Tests whether a specific function is linkable. No execution is required only
building success or fail.
"""

import logging
from typing import Set

from core.database import Database
from core.test import Test, TestType, TestOutcome
from core.function import Function
from core.testgenerator import TestGenerator
from samplers.declare import DeclarationSampler


class FunctionPresenceGenerator(TestGenerator):
    """
    """

    def generate(self) -> Set[Test]:
        """
        Generates all presence test objects for all functions in the database.
        """

        tests = set()

        # find all functions which have not been tested
        functions = filter(lambda f: not f.properties.get('presence_tested', False),
                           Database().functions)

        # for all applicable functions
        for func in functions:
            test = self.generate_test(func)
            tests.add(test)

        return tests

    def generate_test(self, function: Function) -> Test:
        """
        Generates a Test object containing a valid main block and a function call without
        check or print statements.
        """

        logging.info('function presence generating test for %s', function.name)

        # create Test and assign build success/fail closures
        test = Test(f'function_presence_{function.name}', test_type=TestType.BUILD_ONLY)

        test.source = self._gen_main()

        # generate declaration of arguments
        sampler = DeclarationSampler()
        for sample in sampler.generate_samples(function):
            sample.generate_source(test.source)

        # add evaluation closures
        def build_fail():
            function.properties['presence_tested'] = True
            function.properties['present'] = False

            test.build_outcome = TestOutcome.FAIL

        test.build_fail_function = build_fail

        def build_success():
            function.properties['presence_tested'] = True
            function.properties['present'] = True

            test.build_outcome = TestOutcome.SUCCESS

        test.build_success_function = build_success

        return test
