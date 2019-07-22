"""
"""

from typing import Callable, Set, Union, Optional
from enum import Enum
from pathlib import Path

from core.source import Source
from core.variable import Variable

class TestType(Enum):
    BUILD_AND_RUN = 0
    BUILD_ONLY = 1

class TestOutcome(Enum):
    FAILED = 0
    SUCCESS = 1

class Test:
    """
    """

    def __init__(self, name: str, source: Source, test_type: TestType=TestType.BUILD_AND_RUN) -> None:
        self._name: str = name
        self._type: TestType = test_type

        self._source: Source = source
        self._executable: Optional[Path] = None

        # build closures
        self._build_success_func: Optional[Callable[[], None]] = None
        self._build_fail_func: Optional[Callable[[], None]] = None

        # run closures
        self._run_success_func = None
        self._run_fail_func = None

        self._captures: Set[str] = set()
        self._build_outcome: Optional[TestOutcome] = None
        self._run_outcome: Optional[TestOutcome] = None

        # Actual outcome after tested.
        # Until set default value is ''
        # Once tested can be set to pass/fail/xfail/xpass
        #self._result = ''

    @property
    def build_success_function(self) -> Optional[Callable[[], None]]:
        return self._build_success_func
    @build_success_function.setter
    def build_success_function(self, func: Callable[[], None]) -> None:
        self._build_success_func = func

    @property
    def build_fail_function(self) -> Optional[Callable[[], None]]:
        return self._build_fail_func
    @build_fail_function.setter
    def build_fail_function(self, func: Callable[[], None]) -> None:
        self._build_fail_func = func

    @property
    def run_success_function(self):
        return self._run_success_func
    @run_success_function.setter
    def run_success_function(self, func) -> None:
        self._run_success_func = func

    @property
    def run_fail_function(self):
        return self._run_fail_func
    @run_fail_function.setter
    def run_fail_function(self, func) -> None:
        self._run_fail_func = func

    @property
    def captures(self) -> Set[str]:
        return self._captures

    def register_capture(self, token: str) -> None:
        self._captures.add(token)

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> TestType:
        return self._type

    @property
    def source(self) -> Source:
        return self._source
    
    @property
    def executable(self) -> Union[Path, None]:
        return self._executable
    @executable.setter
    def executable(self, path: Path):
        self._executable = path

    @property
    def build_outcome(self) -> Optional[TestOutcome]:
        return self._build_outcome
    @build_outcome.setter
    def build_outcome(self, outcome: TestOutcome) -> None:
        self._build_outcome = outcome 

    @property
    def run_outcome(self) -> Optional[TestOutcome]:
        return self._run_outcome
    @run_outcome.setter
    def run_outcome(self, outcome: TestOutcome) -> None:
        self._run_outcome = outcome 

    def __str__(self) -> str:
        return 'Test: ' + self.name + ' : ' + str(self.type)

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


