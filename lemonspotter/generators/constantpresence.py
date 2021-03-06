"""
This module defines the constant presence test generator.

Tests whether a specific constant exists. No execution is required only building success or fail.
"""

import logging
from typing import Set

from lemonspotter.core.database import Database
from lemonspotter.core.test import Test, TestType, TestOutcome
from lemonspotter.core.testgenerator import TestGenerator
from lemonspotter.core.constant import Constant
from lemonspotter.core.variable import Variable
from lemonspotter.core.statement import (DeclarationAssignmentStatement,
                                         FunctionStatement,
                                         MainDefinitionStatement,
                                         ReturnStatement)


class ConstantPresenceGenerator(TestGenerator):
    """
    This TestGenerator generates tests which check existance and captures the value of a constant.
    """

    def generate(self) -> Set[Test]:
        """
        Generates all constant presence test objects for all constants in the database.
        """

        tests = set()

        # find all functions which have not been tested
        constants = filter(lambda c: not c.properties.get('presence_tested', False),
                           Database().get_constants())

        # for all applicable functions
        for constant in constants:
            test = self.generate_test(constant)

            tests.add(test)

        return tests

    def generate_test(self, constant: Constant) -> Test:
        """
        Generates a Test with a main statement and a variable with the assignment of
        the given constant.
        """

        logging.info('generating constant presence test for %s', constant.name)

        source = self._generate_source_frame()

        block_main = MainDefinitionStatement()
        source.add_at_start(block_main)

        block_main.add_at_end(ReturnStatement('0'))

        variable = Variable(constant.type, f'variable_{constant.name}', constant.name)

        declaration = DeclarationAssignmentStatement(variable,
                                                     'declare variable with constant name')
        block_main.add_at_start(declaration)

        if constant.type.printable:
            block_main.add_at_start(FunctionStatement.generate_print(variable,
                                                                     'extract constant value'))

            test = Test(f'constant_presence_{constant.name}',
                        TestType.BUILD_AND_RUN,
                        source)

        else:
            test = Test(f'constant_presence_{constant.name}',
                        TestType.BUILD_ONLY,
                        source)

        def build_fail():
            constant.properties['presence_tested'] = True
            constant.properties['present'] = False

            test.build_outcome = TestOutcome.FAILED

        test.build_fail_function = build_fail

        def build_success():
            constant.properties['presence_tested'] = True
            constant.properties['present'] = True

            test.build_outcome = TestOutcome.SUCCESS

        test.build_success_function = build_success

        def run_fail():
            test.run_outcome = TestOutcome.FAILED

        test.run_fail_function = run_fail

        def run_success():
            # assign constant value found
            if variable.type.printable and variable.value is None:
                raise RuntimeError('Variable is printable, but no value is set.')

            constant.properties['value'] = variable.value

            # verify against specification
            if not constant.defined:
                test.run_outcome = TestOutcome.SUCCESS

            else:
                if constant.validate():
                    test.run_outcome = TestOutcome.SUCCESS
                else:
                    test.run_outcome = TestOutcome.FAILED

        test.run_success_function = run_success

        return test
