"""
Lemonspotter Runtime
"""

import logging
import json
from pathlib import Path

from lemonspotter.parsers.mpiparser import MPIParser
from lemonspotter.executors.mpiexecutor import MPIExecutor
from lemonspotter.generators.startend import StartEndGenerator
from lemonspotter.generators.constantpresence import ConstantPresenceGenerator
from lemonspotter.generators.functionpresence import FunctionPresenceGenerator
from lemonspotter.samplers.valid import ValidSampler
from lemonspotter.core.report import TestReport


class Runtime:
    """
    This class is the main run time of Lemonspotter.
    """

    def __init__(self, database_path: Path, mpicc: str, mpiexec: str):
        """
        Construct the LemonSpotter runtime
        """

        self.parse_database(database_path)

        self._reporter = TestReport()

        self._executor = MPIExecutor(mpicc=mpicc, mpiexec=mpiexec)

    @property
    def reporter(self):
        return self._reporter

    def parse_database(self, database_path: Path):
        """
        Parse the database pointed to by the command line argument.
        """

        # TODO this is a chicken-egg situation
        # we don't know the MPIParser is required for the database
        # but we need to use a parser to open the database
        parser = MPIParser()
        parser(database_path)

    def presence_testing(self):
        """
        Generate and run the presence testing required for the database.
        """

        # generate all constant presence tests
        generator = ConstantPresenceGenerator()
        constant_tests = generator.generate()

        func_gen = FunctionPresenceGenerator()
        function_tests = func_gen.generate()

        self._executor.execute(constant_tests)
        self._executor.execute(function_tests)

        for test in constant_tests:
            self.reporter.log_test_result(test)

        for test in function_tests:
            self.reporter.log_test_result(test)

    def start_end_testing(self):
        sampler = ValidSampler()

        generator = StartEndGenerator()
        start_end_tests = generator.generate(sampler)

        self._executor.execute(start_end_tests)

        for test in start_end_tests:
            self.reporter.log_test_result(test)
