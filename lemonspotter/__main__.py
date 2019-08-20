import logging
from subprocess import Popen, PIPE
from pathlib import Path
import sys
import argparse
import json

from lemonspotter.core.runtime import Runtime

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
        runtime = Runtime(Path(arguments.specification), arguments.mpicc, arguments.mpiexec)
        runtime.presence_testing()
        runtime.start_end_testing()

        # Prints report and writes to file
        runtime.reporter.print_report()

if __name__ == '__main__':
    main()
