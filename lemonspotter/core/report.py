import datetime
import json
from pathlib import Path
from typing import List, MutableMapping, Mapping, Any

from lemonspotter.core.test import Test
from lemonspotter.core.test import TestType
from lemonspotter.core.test import TestOutcome
from lemonspotter.core.database import Database


class TestReport():
    """
    Class for generating logging statements for tests
    """

    def __init__(self):
        self._now = datetime.datetime.now()
        self._report_id: str = "lsout_" + self._now.strftime("%Y-%m-%d_%H:%M")

        self._report: MutableMapping = {}
        self._tests: List[Test] = []

        # Ensures that report directory exists
        report_dir = Path.resolve(Path(__file__) / '../../../reports')
        if not Path.exists(report_dir):
            Path.mkdir(report_dir)

        # Creates path to report file
        self._report_file_name = self._report_id + '.log'
        self._report_file_dir = Path(report_dir) / self._report_file_name
        self._report_file_dir = Path.resolve(self._report_file_dir)

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

    def generate_report(self) -> None:
        """
        Generates the complete report for tests run to this point
        """

        self._generate_report()

    def _generate_report(self) -> None:
        """"""

        # Generates Presence Report #
        presence_report: MutableMapping[str, Mapping[str, Any]] = {}

        constants = {}
        for constant in Database().get_constants():
            constants[constant.name] = constant.properties

        functions = {}
        for function in Database().get_functions():
            functions[function.name] = function.properties

        presence_report['constants'] = constants
        presence_report['functions'] = functions

        self._report['presence_report'] = presence_report

        test_report = {}
        for test in self._tests:
            test_report[test.name] = {'type': str(test.type),
                                      'build_outcome': str(test.build_outcome),
                                      'run_outcome': str(test.run_outcome)}

        self._report['tests'] = test_report

    def print_report(self, indent=2):
        """
        Pretty prints report
        """

        self._generate_report()
        print(json.dumps(self._report, indent=indent))

    def write_report(self):
        """
        Writes generated report to file
        """

        self._generate_report()
        with open(self.report_file_dir, 'a+') as file_buffer:
            json.dump(self._report, file_buffer)
