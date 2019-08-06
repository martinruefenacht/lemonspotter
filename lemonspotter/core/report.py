import os
import datetime
import json

from typing import List
from core.test import Test
from core.test import TestType
from core.test import TestOutcome


class TestReport():
    """
    Class for generating logging statements for tests
    """
    def __init__(self, database):
        self._now = datetime.datetime.now()
        self._report_id: str = "lsout_" + self._now.strftime("%Y-%m-%d_%H:%M")
        self._database = database

        self._report = {}
        self._tests = []

        # Ensures that report directory exists
        report_dir = os.path.abspath(os.path.join(__file__,
                                                  '../../../reports'))
        if not os.path.exists(report_dir):
            os.mkdir(report_dir)

        # Creates path to report file
        self._report_file_name: str = self._report_id + '.log'
        self._report_file_dir: str = os.path.join(report_dir, self._report_file_name)
        self._report_file_dir: str = os.path.abspath(self._report_file_dir)

    @property
    def report_id(self) -> str:
        return self._report_id

    @report_id.setter
    def report_id(self, report_id) -> None:
        self._report_id = report_id

    @property
    def report_file_dir(self) -> str:
        return self._report_file_dir

    @report_file_dir.setter
    def report_file_dir(self, report_file_dir) -> None:
        self._report_file_dir = report_file_dir

    @property
    def tests(self) -> List[Test]:
        return self._tests

    @tests.setter
    def tests(self, tests) -> None:
        self._tests = tests

    def log_test_result(self, test, msg=None) -> None:
        """
        Prints results for single test
        """

        if test not in self.tests:
            self.tests.append(test)

        log_msg = ''
        if test.type == TestType.BUILD_ONLY:
            log_msg += '[BUILD ONLY|'
            if test.build_outcome == TestOutcome.SUCCESS:
                log_msg += 'PASS|'
            else:
                log_msg += 'FAIL|'
        elif test.type == TestType.BUILD_AND_RUN:
            log_msg += '[RUN|'
            if test.run_outcome == TestOutcome.SUCCESS:
                log_msg += 'PASS|'
            else:
                log_msg += 'FAIL|'

        log_msg += test.name + ']'
        if msg:
            log_msg += '\n\t ' + msg

        print(log_msg)

    @property
    def generate_presence_report(self) -> None:
        """
        Generates presence_report to report file
        """
        presence_report = {}

        constants = {}
        for constant in self._database.constants:
            constants[constant.name] = constant.properties

        functions = {}
        for function in self._database.functions:
            functions[function.name] = function.properties

        presence_report['constants'] = constants
        presence_report['functions'] = functions

        self._report['presence_report'] = presence_report


    @property
    def generate_report(self) -> None:
        """
        Generates the complete report for tests run to this point
        """
        self._generate_report()


    def _generate_report(self) -> None:
        self.generate_presence_report


    @property
    def print_report(self):
        """
        Pretty prints report
        """
        self._generate_report()
        print(json.dumps(self._report, indent=4))


    @property
    def write_report(self):
        """
        Writes generated report to file
        """
        self._generate_report()
        with open(self.report_file_dir, 'a+') as file_buffer:
            json.dump(self._report, file_buffer)


