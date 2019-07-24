"""
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

# TODO rethink these?
from parsers.mpiparser import MPIParser
from executors.mpiexecutor import MPIExecutor
from core.database import Database

#from generators.startend import StartEndGenerator
from generators.constantpresence import ConstantPresenceGenerator
from generators.functionpresence import FunctionPresenceGenerator

from core.report import TestReport

class LemonSpotter:
    """
    """

    def __init__(self, database_path: Path, mpicc: str, mpiexec: str):
        """
        Construct the LemonSpotter runtime.
        """

        self._database: Optional[Database] = None
        self.parse_database(database_path)

        self._reporter = TestReport(self._database)

        self._executor = MPIExecutor(mpicc=mpicc, mpiexec=mpiexec, reporter=self._reporter)

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

    def presence_report(self) -> str:
        """
        """

        report = ''

        if self._database:
            for constant in self._database.constants:
                report += constant.name + '\t\t ' + str(constant.properties) + '\n'

            report += '\n' + '#' * 80 + '\n\n'

            for function in self._database.functions:
                report += function.name + '\t\t ' + str(function.properties) + '\n'

            return report

        raise RuntimeError('No database to report.')

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
        results = self._executor.build(tests=self.tests)

    def run_tests(self):
        results = self._executor.run(tests=self.tests)

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

    # database arguments
    parser.add_argument('database',
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

    # initialize and load the database
    runtime = LemonSpotter(Path(arguments.database), arguments.mpicc, arguments.mpiexec)

    # perform presence testing
    runtime.presence_testing()
    
    # Log presence report to file
    runtime._reporter.write_presence_report()

    #runtime.generate_tests()
    #runtime.build_tests()
    #runtime.run_tests()

if __name__ == '__main__':
    main()
