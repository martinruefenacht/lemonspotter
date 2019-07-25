"""
This module defines the constant presence test generator.

Tests whether a specific constant exists. No execution is required only building success or fail.
"""

import logging
from typing import Set

from core.database import Database
from core.test import Test, TestType, TestOutcome
from core.testgenerator import TestGenerator
from core.constant import Constant
from core.variable import Variable

from core.statement import DeclarationStatement, AssignmentStatement, FunctionStatement


class ConstantPresenceGenerator(TestGenerator):
    """
    This TestGenerator generates tests which check existance and captures the value of a constant.
    """

    def __init__(self, database: Database) -> None:
        super().__init__(database)

    def generate(self) -> Set[Test]:
        """
        Generates all constant presence test objects for all constants in the database.
        """

        tests = set()

        # find all functions which have not been tested
        constants = filter(lambda c: not c.properties.get('presence_tested', False),
                           self._database.constants)

        # for all applicable functions
        for constant in constants:
            test = self.generate_test(constant)

            logging.debug('test generated for %s:\n' + repr(test.source).replace('%', '%%'),
                          constant.name)

            tests.add(test)

        return tests

    def generate_test(self, constant: Constant) -> Test:
        """
        Generates a Test with a main statement and a variable with the assignment of
        the given constant.
        """

        source = self.generate_main()

        variable = Variable(constant.type, 'variable_' + constant.name)

        declaration = DeclarationStatement(variable)
        source.add_at_start(declaration)

        variable.value = constant.name
        assignment = AssignmentStatement(variable)
        source.add_at_start(assignment)

        if constant.type.printable:
            source.add_at_start(FunctionStatement.generate_print(variable))

            test = Test('constant_presence_' + constant.name,
                        source,
                        test_type=TestType.BUILD_AND_RUN)

            test.register_capture(variable)

        else:
            test = Test('constant_presence_' + constant.name,
                        source,
                        test_type=TestType.BUILD_ONLY)

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

            logging.info('test %s successful', test.name)

        test.run_success_function = run_success

        return test
