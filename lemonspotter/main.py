import sys
import argparse
import logging

from parsers.mpiparser import MPIParser
from generators.startend import StartEndGenerator
from executors.mpiexecutor import MPIExecutor

class LemonSpotter:
    def __init__(self):
        """
        Construct the LemonSpotter runtime.
        """

        self._database = None
        self.tests = []

        self.parse_arguments()
        self.set_logging_level()

        self.parse_database()

        #TODO self.extract_constants()

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    @database.deleter
    def database(self):
        del self._database

    def parse_arguments(self):
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

        self.arguments = parser.parse_args()

        if not self.arguments:
            parser.print_help()
            sys.exit(0)

    def set_logging_level(self):
        """
        Set the logging level to the one specified on the command line.
        """

        numeric_level = getattr(logging, self.arguments.log.upper(), None)

        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % self.arguments.log)

        logging.basicConfig(level=numeric_level)

    def parse_database(self):
        """
        Parse the database pointed to by the command line argument.
        """

        parser = MPIParser()

        self.database = parser(self.arguments.database)

    def extract_constants(self):
        """
        Generate and run an extraction program to determine the values of
        constants and errors.
        """
        raise NotImplementedError

    def generate_tests(self):
        generator = StartEndGenerator(self.database)
        
        # TODO instantiator make it a functioning object
        instantiator = None
        self.tests.extend(list(generator.generate(instantiator)))

        logging.debug('generated tests:')
        for test in self.tests:
            for source in test.sources:
                logging.debug(source.get_source())

        for test in self.tests:
            for source in test.sources:
                source.write()

    def build_tests(self):
        executor = MPIExecutor()
        executor.build(tests=self.tests)

    def run_tests(self):
        executor = MPIExecutor()
        results = executor.run(tests=self.tests)

        for key, value in results.items():
            print(key + ", " + value[0])


def main():
    """
    """

    runtime = LemonSpotter()

    runtime.generate_tests()
    runtime.build_tests()
    runtime.run_tests()

if __name__ == '__main__':
    main()
