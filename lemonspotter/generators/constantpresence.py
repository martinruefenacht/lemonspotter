"""
This module defines the constant presence test generator.

Tests whether a specific constant exists. No execution is required only building success or fail.
"""

import logging
from typing import Set

from core.database import Database
from core.test import Test, TestType
from core.source import Source
from core.testgenerator import TestGenerator
from core.constant import Constant
from core.variable import Variable

from core.statement import DeclarationStatement, AssignmentStatement

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
        constants = filter(lambda c: not c.properties.get('presence_tested', False), self._database.constants)

        # for all applicable functions
        for constant in constants:
            test = self.generate_test(constant)

            logging.debug(('constant test generated for %s:\n' + repr(test.source)), constant.name)

            tests.add(test)

        return tests

    def generate_test(self, constant: Constant) -> Test:
        """
        Generates a Test with a main statement and a variable with the assignment of the given constant.
        """

        source = self.generate_main()

        # TODO convert to object db
        variable = Variable(self._database.types_by_abstract_type[constant.abstract_type], 'variable')

        declaration = DeclarationStatement(variable) 
        source.add_at_start(declaration)

        assignment = AssignmentStatement(variable.name, constant.name);
        source.add_at_start(assignment)

        # potential to combine presence and capture output
        # add print statement 
        #source.add_at_start(variable.generate_print_statement())

        test = Test('constant_presence_' + constant.name, source, test_type=TestType.BUILD_ONLY)

        def build_fail():
            constant.properties['presence_tested'] = True
            constant.properties['present'] = False
        test.build_fail_function = build_fail;

        def build_success():
            constant.properties['presence_tested'] = True
            constant.properties['present'] = True
        test.build_success_function = build_success

        return test
