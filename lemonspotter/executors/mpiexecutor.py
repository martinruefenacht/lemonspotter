import os

from pathlib import Path
import logging
from subprocess import Popen, PIPE
from typing import Set, List

from core.test import Test, TestType


class MPIExecutor:
    def __init__(self, mpicc: str, mpiexec: str, test_directory: Path = Path('tests/')):
        """
        Initializes a test executor for MPI Libraries
        """

        self._test_directory = test_directory.resolve()

        self._mpicc = mpicc
        self._mpiexec = mpiexec

    @property
    def test_directory(self):
        """
        Gets the directory where tests will be found/executed in
        """
        return self._test_directory

    def execute(self, tests: Set[Test]):
        """
        """

        # check for test directory
        if not os.path.isdir(self.test_directory):
            os.makedirs(self.test_directory)

        if tests:
            try:
                for test in tests:
                    self.build_test(test)

            except FileNotFoundError as error:
                logging.error(error)
                logging.error('Building set of tests failed.')
                return

            try:
                for test in tests:
                    self.run_test(test)

            except FileNotFoundError as error:
                logging.error(error)
                logging.error('Runnign set of test failed.')
                return

    def build_test(self, test: Test, arguments: List[str] = []) -> None:
        logging.info('building test %s', test.name)

        if test.build_outcome:
            logging.critical('Test %s has build outcome.', test.name)
            return

        # output source file
        test_filename = self._test_directory / (test.name + '.c')
        test.source.write(Path(test_filename))

        # create executable command
        executable_filename = self.test_directory / test.name
        command = [self._mpicc, str(test_filename)] + arguments + ["-o", str(executable_filename)]

        logging.debug('executing: %s', ' '.join(command))

        # execute command
        try:
            process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)  # type: ignore
            stdout, stderr = process.communicate()

        except FileNotFoundError as error:
            logging.error('Test %s failed to build, due to missing mpicc.', test.name)

            raise error

        # evaluate build result
        logging.debug('build stdout:\n%s\n', stdout)
        logging.debug('build stderr:\n%s\n', stderr)

        if not stdout and not stderr:
            # set executable on test
            test.executable = Path(executable_filename)

            test.build_success_function()

            logging.debug('success building %s', test.name)

        else:
            # TODO evalulate build output, is there ERROR?
            test.build_fail_function() 

            logging.warning('building failed of test %s', test.name)

    def run_test(self, test: Test, arguments: List[str] = []) -> None:
        """
        """

        # TODO test should define how many processes it needs
        # TODO check it is <= available with current run
        # TODO testgenerators should not generate any tests with more
        arguments = ['-n', '1']

        # check if valid test
        if test.type is TestType.BUILD_ONLY:
            logging.info('skip running test %s due to BUILD_ONLY', test.name)

        elif test.run_outcome:
            logging.critical('Test %s has run outcome.', test.name)
            return

        else:
            logging.debug('preparing test %s.', test.name)

            # create command
            command = [self._mpiexec] + arguments + [str(test.executable)]

            # run test executable
            logging.debug('executing "%s"', ' '.join(command))
            try:
                process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)  # type: ignore
                stdout, stderr = process.communicate()

            except FileNotFoundError as error:
                logging.error(error)
                logging.error('skip running test %s', test.name)
                return

            logging.debug('run stdout:\n%s\n', stdout)
            logging.debug('run stderr:\n%s\n', stderr)

            # test run check
            if not stderr and process.returncode == 0:
                # filter for captures
                logging.debug('test capturing: %s', str(test.captures))
                for line in stdout.split('\n'):
                    if line:
                        tokens = line.split()
                        logging.debug(str(tokens))

                        variable = test.captures.get(tokens[0], None)
                        if variable is not None:
                            # currently only supports key-value captures
                            variable.value = tokens[1]
                            logging.debug('captured %s = %s', variable.name, tokens[1])

                # call success function
                test.run_success_function()
                logging.info('running test %s successful', test.name)

                return

            elif process.returncode > 0:
                logging.critical('test crashed with errorcode %i', process.returncode)

            else:
                logging.warning('test %s failed with internal error.', test.name)

            test.run_fail_function()
