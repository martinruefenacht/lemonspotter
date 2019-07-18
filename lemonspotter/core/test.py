"""
"""

from pathlib import Path
from enum import Enum

from core.source import Source
from core.variable import Variable

class TestType(Enum):
    BUILD_AND_RUN = 0
    BUILD_ONLY = 1

class TestOutcome(Enum):
    FAILED_BUILD = 0
    CRASH = 1
    SUCCESS = 2

class Test:
    """
    """

    def __init__(self, name: str, source: Source, test_type: TestType=TestType.BUILD_AND_RUN):
        self._name = name
        self._source = source
        self._test_type = test_type

        # build closures
        self._build_success_func = None
        self._build_fail_func = None

        # run closures
        self._run_success_func = None
        self._run_fail_func = None

        self._build_results = []
        self._exec_results = []

        # Actual outcome after tested.
        # Until set default value is ''
        # Once tested can be set to pass/fail/xfail/xpass
        self._result = ''

    @property
    def build_success_function(self):
        return self._build_success_func
    @build_success_function.setter
    def build_success_function(self, func):
        self._build_success_func = func

    @property
    def build_fail_function(self):
        return self._build_fail_func
    @build_fail_function.setter
    def build_fail_function(self, func):
        self._build_fail_func = func

    @property
    def run_success_function(self):
        return self._run_success_func
    @run_success_function.setter
    def run_success_function(self, func):
        self._run_success_func = func

    @property
    def run_fail_function(self):
        return self._run_fail_func
    @run_fail_function.setter
    def run_fail_function(self, func):
        self._run_fail_func = func


    def write(self, path: Path) -> None:
        """
        Write this tests C source code to the given path.
        """

        with path.open() as source_file:
            source_file.write(self.source)

    def add_capture(self, variable: Variable):
        """
        Register variable output to be caught.
        """

        self.captures.add(variable)

    @property
    def build_only(self):
        return self._build_only

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        del self._name

    @property
    def source(self):
        return self._source

    @property
    def build_results(self):
        return self._build_results

    @build_results.setter
    def build_results(self, build_results):
        self._build_results = build_results

    @build_results.deleter
    def build_results(self):
        del self._build_results

    @property
    def exec_results(self):
        return self._exec_results

    @exec_results.setter
    def exec_results(self, exec_results):
        self._exec_results = exec_results

    @exec_results.deleter
    def exec_results(self):
        del self._exec_results

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = result

    @result.deleter
    def result(self):
        del self._result



#    def write(self):
#        """
#        Writes source object to file that can be compiled/run
#        by executors.
#        """
#
#        # TODO this is hard coding paths
#
#        if not os.path.isdir('../tests'):
#            os.makedirs("../tests")
#
#        file_name = self.name + ".c"
#        test_file = open("../tests/" + file_name, "w+")
#
#        for line in self.get_source():
#            test_file.write(line+"\n")
#
#        test_file.close()

    def build_result_parser(self):
        """
        Fails test if build process produces error
        """
        if self.build_results[1]:
            print("BUILD ERROR: " + self.name + " failed to build.")
            self.result = "failed"

    def exec_result_parser(self):
        """
        Parses output of test execution into results
        """
        if self.expected_result == 'pass':
            if self.exec_results[1]:
                print("STDERR Not Empty")
                print(self.exec_results[1])


