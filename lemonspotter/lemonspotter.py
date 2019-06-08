import sys
import argparse
import logging

import core
import parsers.mpiparser
import generators.startend as startend

class LemonSpotter:
    def __init__(self):
        """Construct the LemonSpotter runtime."""

        self.database = None

        self.parse_arguments()
        self.set_logging_level()

        self.parse_database()

        #TODO self.extract_constants()
        
    def parse_arguments(self):
        """Parse the arguments given on the command line."""

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
        """Set the logging level to the one specified on the command line."""

        numeric_level = getattr(logging, self.arguments.log.upper(), None)
        
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % self.arguments.log)
        
        logging.basicConfig(level=numeric_level)

    def parse_database(self):
        """Parse the database pointed to by the command line argument."""

        parser = parsers.mpiparser.MPIParser()

        self.database = parser(self.arguments.database)

    def extract_constants(self):
        """
        Generate and run an extraction program to determine the values of
        constants and errors.
        """
        
        raise NotImplementedError

    def generate_tests(self):
        generator = startend.StartEndGenerator(self.database)

        sources = generator.generate()
        
        for source in sources:
            print('\n'.join(source.source_lines))

    def build_tests(self):
        raise NotImplementedError

    def run_tests(self):
        raise NotImplementedError

if __name__ == '__main__':
    ls = LemonSpotter()

    ls.generate_tests()
