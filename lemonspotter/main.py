"""
Lemonspotter Runtime
"""

import sys
import argparse
import logging
from subprocess import Popen, PIPE
from pathlib import Path
from typing import Optional

# TODO rethink these?
from parsers.mpiparser import MPIParser
from executors.mpiexecutor import MPIExecutor
from core.database import Database

# from generators.startend import StartEndGenerator
from generators.constantpresence import ConstantPresenceGenerator
from generators.functionpresence import FunctionPresenceGenerator

from core.report import TestReport


class LemonSpotter:
    """
    Lemonspotter Runtime Object
    """

    def __init__(self, database_path: Path, mpicc: str, mpiexec: str):
        """
        Construct the LemonSpotter runtime
        """

        self._database: Optional[Database] = None
        self.parse_database(database_path)

        self._reporter = TestReport(self._database)

        self._executor = MPIExecutor(mpicc=mpicc, mpiexec=mpiexec)

    @property
    def database(self):
        return self._database

    def parse_database(self, database_path: Path):
        """
        Parse the database pointed to by the command line argument.
        """

        parser = MPIParser()
        self._database = parser(database_path)

    def presence_testing(self):
        """
        Generate and run the presence testing required for the database.
        """

        # generate all constant presence tests
        generator = ConstantPresenceGenerator(self.database)
        constant_tests = generator.generate()

        func_gen = FunctionPresenceGenerator(self.database)
        function_tests = func_gen.generate()

        self._executor.execute(constant_tests)
        self._executor.execute(function_tests)

        for test in constant_tests:
            self._reporter.log_test_result(test)

        for test in function_tests:
            self._reporter.log_test_result(test)

    def generate_tests(self):
        pass
#        generator = StartEndGenerator(self.database)
#
#        # TODO instantiator make it a functioning object
#        instantiator = None
#        self.tests = []
#        self.tests.extend(list(generator.generate(instantiator)))
#
#        logging.debug('generated tests:')
#        for test in self.tests:
#            if not test:
#                logging.warning('test is none')
#                continue
#
#            for source in test.sources:
#                logging.debug(source.get_source())
#                source.write()

    def build_tests(self):
        self._executor.build(tests=self.tests)

    def run_tests(self):
        self._executor.run(tests=self.tests)


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

    parser.add_argument('--test',
                        action='store_true',
                        dest='test',
                        default=False,
                        help='Runs Lemonspotter Unit Tests')

    # database arguments
    parser.add_argument('database',
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


def main():
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
        process = Popen('flake8', stdout=PIPE, stderr=PIPE, cwd='../')
        stdout, stderr = process.communicate()
        print(stdout.decode('utf-8'))
    elif not arguments.database:
        logging.error("Database path not defined")
    else:
        # initialize and load the database
        runtime = LemonSpotter(Path(arguments.database), arguments.mpicc, arguments.mpiexec)

        # perform presence testing
        runtime.presence_testing()

        # Prints report and writes to file
        runtime._reporter.print_report
        runtime._reporter.write_report


if __name__ == '__main__':
    main()
