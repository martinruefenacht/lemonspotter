import os

from pathlib import Path
import logging
from subprocess import Popen, PIPE
from typing import Set, List

from core.test import Test, TestOutcome, TestType

class MPIExecutor:
    def __init__(self, mpicc: str, mpiexec: str, test_directory='tests/'):
        """
        Initializes a test executor for MPI Libraries
        """

        self._test_directory = os.path.abspath(test_directory)

        #self._build_results = {}
        #self._exec_results = {}

        self._mpicc = mpicc
        self._mpiexec = mpiexec

    @property
    def test_directory(self):
        """
        Gets the directory where tests will be found/executed in
        """
        return self._test_directory

    @test_directory.setter
    def test_directory(self, test_directory):
        """
        Sets the directory where tests will be found/executed in

        """
        self._test_directory = test_directory

    @test_directory.deleter
    def test_directory(self):
        """
        Deletes the directory where tests will be found/executed in
        """
        del self._test_directory

    def execute(self, tests: Set[Test]):
        """
        """

        # check for test directory
        if not os.path.isdir(self.test_directory):
            os.makedirs(self.test_directory)

        if tests:
            for test in tests:
                self.build_test(test)

            for test in tests:
                self.run_test(test)

    def build_test(self, test: Test, arguments: List[str]=[]) -> None:
        logging.info('building test %s', test.name)

        if test.build_outcome != TestOutcome.UNTESTED:
            logging.critical('Test %s has build outcome.', test.name)
            return

        # output source file
        test_filename = self._test_directory + '/' + test.name + ".c"
        test.source.write(Path(test_filename))

        # create executable command
        executable_filename = self.test_directory + '/' + test.name
        command = [self._mpicc, test_filename] + arguments + ["-o", executable_filename]

        logging.info('executing: %s', ' '.join(command))

        # execute command
        try:
            process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)
            stdout, stderr = process.communicate()

        except FileNotFoundError as error:
            logging.error(error)
            logging.error('skip building test %s', test.name)
            return

        # evaluate build result
        logging.debug('build stdout:\n%s\n', stdout)
        logging.debug('build stderr:\n%s\n', stderr)

        if not stdout and not stderr:
            # set executable on test
            test.executable = Path(executable_filename)

            test.build_success_function()

            logging.info('building successful')

        else:
            # TODO evalulate build output, is there ERROR?
            test.build_fail_function()

            logging.warning('building failed')

    def run_test(self, test: Test, arguments: List[str]=[]) -> None:
        """
        """

        # TODO test should define how many processes it needs
        arguments = ['-n', '1']

        # check if valid test
        if test.type is TestType.BUILD_ONLY:
            logging.info('skip running test %s due to BUILD_ONLY', test.name)

        elif test.run_outcome != TestOutcome.UNTESTED:
            logging.critical('Test %s has run outcome.', test.name)

        else:
            logging.info('preparing test %s.', test.name)

            # create command
            command = [self._mpiexec] + arguments + [str(test.executable)]

            # run test executable
            logging.info('executing "%s"', ' '.join(command))
            try:
                process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)
                stdout, stderr = process.communicate()

            except FileNotFoundError as error:
                logging.error(error)
                logging.error('skip running test %s', test.name)
                return

            logging.debug('run stdout:\n%s\n', stdout)
            logging.debug('run stderr:\n%s\n', stderr)

            # test run check
            if not stderr and process.returncode == 0:
                logging.info('test %s successfully run.', test.name)

                # filter for captures
                captured = {}
                for line in stdout.split('\n'):
                    if line:
                        tokens = line.split()

                        logging.debug(str(tokens))
                        logging.debug(test.captures)

                        if tokens[0] in test.captures:
                            # only supports capturing single value
                            captured[tokens[0]] = tokens[1]

                # call success function
                test.run_success_function(captured)
                return

            elif process.returncode > 0:
                logging.critical('test crashed')

            else:
                logging.warning('test %s failed with internal error.', test.name)

            test.run_fail_function()
