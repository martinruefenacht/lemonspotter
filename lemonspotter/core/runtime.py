"""
Lemonspotter Runtime
"""

import sys
import argparse
import logging
import json
from subprocess import Popen, PIPE
from pathlib import Path

from parsers.mpiparser import MPIParser
from executors.mpiexecutor import MPIExecutor
from generators.startend import StartEndGenerator
from generators.constantpresence import ConstantPresenceGenerator
from generators.functionpresence import FunctionPresenceGenerator
from samplers.valid import ValidSampler
from core.report import TestReport


class LemonSpotter:
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


def parse_arguments():
    """
    Parse the arguments given on the command line.
    """

    parser = argparse.ArgumentParser(prog='LemonSpotter')

    # general flags
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s 0.1',
                        help='Print version of LemonSpotter')

    parser.add_argument('--log',
                        default='warning',
                        type=str,
                        help='Set the python logging level.')

    parser.add_argument('--keep',
                        action='store_true',
                        help='Keep C source filesafter tests.')

    parser.add_argument('--dry-run',
                        action='store_true',
                        help='Do everything except execute tests.')

    # mpi flags
    parser.add_argument('--mpicc',
                        default='mpicc',
                        type=str,
                        help='Use specific mpicc.')

    parser.add_argument('--mpiexec',
                        default='mpiexec',
                        type=str,
                        help='Use specific mpiexec.')

    # test flags
    parser.add_argument('--tests',
                        type=str,
                        help='Comma separated list of generators.')

    parser.add_argument('--flake8',
                        action='store_true',
                        dest='flake',
                        default=False,
                        help='Runs flake8 test on Lemonspotter project')

    parser.add_argument('--mypy',
                        action='store_true',
                        dest='mypy',
                        default=False,
                        help='Runs the mypy type checker on LemonSpotter.')

    parser.add_argument('--pytest',
                        action='store_true',
                        dest='pytest',
                        default=False,
                        help='Run the LemonSpotter test suite.')

    parser.add_argument('--test',
                        action='store_true',
                        dest='test',
                        default=False,
                        help='Runs Lemonspotter Unit Tests')

    parser.add_argument('--report',
                        action='store_true',
                        dest='report',
                        default=False,
                        help='Prints report file specified')

    # database arguments
    parser.add_argument('specification',
                        nargs='?',
                        type=str,
                        help='Path to database to use.')

    arguments = parser.parse_args()

    # check for valid input
    if not arguments:
        parser.print_help()
        sys.exit(0)

    return arguments


def set_logging_level(log_level: str):
    """
    Set the logging level to the one specified on the command line.
    """

    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)

    logging.basicConfig(level=numeric_level)


def main() -> None:
    """
    This function is the workflow of LemonSpotter.
    """

    # handle environment
    arguments = parse_arguments()
    set_logging_level(arguments.log)

    # perform presence testing

    if arguments.test:
        raise NotImplementedError

    elif arguments.flake:
        command = [sys.executable, '-m', 'flake8']

        logging.info('executing flake8 with %s', ' '.join(command))
        process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)  # type: ignore

        stdout, stderr = process.communicate()
        print(stdout)

        if stderr:
            logging.error(stderr)

    elif arguments.mypy:
        command = [sys.executable, '-m', 'mypy', __file__]

        logging.info('executing mypy with %s', ' '.join(command))
        process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)  # type: ignore

        stdout, stderr = process.communicate()
        print(stdout)

        if stderr:
            logging.error(stderr)

    elif arguments.pytest:
        command = [sys.executable, '-m', 'pytest']

        logging.info('executing test suite...')
        process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)  # type: ignore

        stdout, stderr = process.communicate()
        print(stdout)

        if stderr:
            logging.error(stderr)

    elif arguments.report:
        with open(arguments.specification) as report_file:
            report = json.load(report_file)

        print(json.dumps(report, indent=2))

    elif not arguments.specification:
        logging.error("Database path not defined")

    else:
        # initialize and load the database
        runtime = LemonSpotter(Path(arguments.specification), arguments.mpicc, arguments.mpiexec)
        runtime.presence_testing()
        runtime.start_end_testing()

        # Prints report and writes to file
        runtime.reporter.print_report()


if __name__ == '__main__':
    main()
