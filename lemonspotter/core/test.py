"""
This modules defines the Test class.
"""

from typing import Callable, Set, Optional
from enum import Enum
from pathlib import Path

from core.source import Source

class TestType(Enum):
    """This Enumeration stores the type of tests available."""

    BUILD_AND_RUN = 0
    BUILD_ONLY = 1

class TestStage(Enum):
    """This Enumeration stores the stages of testing."""

    BUILD = 0
    RUN = 1

class TestOutcome(Enum):
    """This Enumeration stores the type of test outcomes."""

    FAILED = 0
    SUCCESS = 1

class Test:
    """
    This class represents a single Test case. Metadata is stored in the Test while Source stores
    source code level information.
    """

    def __init__(self, name: str, source: Source, test_type: TestType) -> None:
        self._name: str = name
        self._type: TestType = test_type
        self._stage: Optional[TestStage] = None

        self._source: Source = source
        self._executable: Optional[Path] = None

        self._build_success_func: Optional[Callable[[], None]] = None
        self._build_fail_func: Optional[Callable[[], None]] = None

        self._run_success_func: Optional[Callable[[], None]] = None
        self._run_fail_func: Optional[Callable[[], None]] = None

        self._captures: Set[str] = set()

        self._build_outcome: Optional[TestOutcome] = None
        self._run_outcome: Optional[TestOutcome] = None

    @property
    def build_success_function(self) -> Optional[Callable[[], None]]:
        """This property provides access to the build success callback."""

        return self._build_success_func

    @build_success_function.setter
    def build_success_function(self, func: Callable[[], None]) -> None:
        """This provides setting the build success function."""

        self._build_success_func = func

    @property
    def build_fail_function(self) -> Optional[Callable[[], None]]:
        """This property provides access of the build failure function."""

        return self._build_fail_func

    @build_fail_function.setter
    def build_fail_function(self, func: Callable[[], None]) -> None:
        """This provides setting the build failure function."""

        self._build_fail_func = func

    @property
    def run_success_function(self):
        """This property provides access to the run success callback."""

        return self._run_success_func

    @run_success_function.setter
    def run_success_function(self, func) -> None:
        """This provides setting the run success callback."""

        self._run_success_func = func

    @property
    def run_fail_function(self):
        """This property provides access to the run fail callback."""
        return self._run_fail_func

    @run_fail_function.setter
    def run_fail_function(self, func) -> None:
        """This provides setting the run fail callback."""
        self._run_fail_func = func

    @property
    def captures(self) -> Set[str]:
        """This property provides access to the defined captures of the test."""

        return self._captures

    def register_capture(self, token: str) -> None:
        """This method allows registering a capture from the stdout."""

        self._captures.add(token)

    @property
    def name(self) -> str:
        """This property provides the name of the Test."""

        return self._name

    @property
    def type(self) -> TestType:
        """This property provides the TestType of the Test."""

        return self._type

    @property
    def source(self) -> Source:
        """This property provides the Source of the Test."""

        return self._source

    @property
    def executable(self) -> Optional[Path]:
        """This property provides the executable Path."""

        return self._executable

    @executable.setter
    def executable(self, path: Path):
        """This allows setting the executable Path."""
        self._executable = path

    @property
    def stage(self) -> Optional[TestStage]:
        """This property returns the current stage of testing"""
        return self._stage

    @stage.setter
    def stage(self, stage: TestStage):
        """This allows setting the build stage"""
        self._stage = stage

    @property
    def build_outcome(self) -> Optional[TestOutcome]:
        """This property provides the build outcome."""
        return self._build_outcome

    @build_outcome.setter
    def build_outcome(self, outcome: TestOutcome) -> None:
        """This allows setting the build outcome."""

        self._build_outcome = outcome

    @property
    def run_outcome(self) -> Optional[TestOutcome]:
        """This property provides the run outcome."""

        return self._run_outcome

    @run_outcome.setter
    def run_outcome(self, outcome: TestOutcome) -> None:
        """This allows setting the run outcome."""

        self._run_outcome = outcome

    def __str__(self) -> str:
        return 'Test: ' + self.name + ' : ' + str(self.type)
