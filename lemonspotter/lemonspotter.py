import sys
import argparse
import logging

import lemonspotter.core as core
import lemonspotter.parsers as parsers
import lemonspotter.generators as generators

class LemonSpotter:
    def __init__(self):
        self.database = None

        self.parse_arguments()
        self.set_logging_level()

        self.parse_database()

        #TODO self.extract_constants()
        
    def parse_arguments(self):
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

        # database arguments
        parser.add_argument('database',
                            type=str,
                            help='Path to database to use.')

        self.arguments = parser.parse_args()

        if not self.arguments:
            parser.print_help()
            sys.exit(0)

    def set_logging_level(self):
        numeric_level = getattr(logging, self.arguments.log.upper(), None)
        
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % self.arguments.log)
        
        logging.basicConfig(level=numeric_level)

    def parse_database(self):
        parser = parsers.MPIParser(self.arguments.database)

        self.database = parser.load_database()

    def extract_constants(self):
        raise NotImplementedError

    def generate_tests(self):
        # use generator to generate C source code
        # as string
        # output to file if wanted/needed
        raise NotImplementedError

    def build_tests(self):
        raise NotImplementedError

    def run_tests(self):
        raise NotImplementedError
