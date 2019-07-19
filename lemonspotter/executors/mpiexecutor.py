import os

from pathlib import Path
import logging
from subprocess import Popen, PIPE
from typing import Set, List

from core.test import Test

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

    def build(self, tests: Set[Test], arguments: List[str]=[]) -> None:
        """
        Builds a test into a runnable executable

        tests: list of test objects that define the tests to run
        """

        # make directory if not exists
        if not os.path.isdir(self.test_directory):
            os.makedirs(self.test_directory)

        # build tests if any
        if tests:
            for test in tests:
                self.build_test(test, arguments)
                
#        else:
#            # DEPRECATED
#            # This behavior works currently for compatability.
#            files = pathlib.Path(self.test_directory).glob('**/*.c')
#            for test in files:
#                test_name = str(test)[len(self._test_directory): len(str(test))-2]
#                # Generate MPICC command that compiles test excutable
#                mpicc = ["mpicc", str(test)] + args + ["-o", self.test_directory, test_name]
#
#                process = Popen(mpicc, shell=True, stdout=PIPE, stderr=PIPE)
#                self.build_results[test_name] = [str(stdout).decode('UTF-8'),
#                                                 str(stderr).decode('UTF-8')]

        #return self.build_results

    def build_test(self, test: Test, arguments: List[str]=[]):
        logging.info('building test %s', test.name)

        # output source file
        test_filename = self._test_directory + '/' + test.name + ".c"
        test.write(Path(test_filename))

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
            logging.error('skipping test %s', test.name)
            return

        # evaluate build result
        logging.debug('stdout\n%s', stdout)
        logging.debug('stderr\n%s', stderr)

        if not stdout and not stderr:
            test.build_success_function()

            logging.info('building successful')

        else:
            # TODO evalulate build output, is there ERROR?
            test.build_fail_function()

            logging.warning('building failed')

    def run(self, tests=[], args=[]):

        if not os.path.isdir(self.test_directory):
            os.makedirs(self.test_directory)

        if tests:
            # Runs if a defined list of tests to run is passed into run()
            for test in tests:
                if not test.result:
                    mpiexec = ["mpiexec"] + args + [self.test_directory + test.name]
                    process = Popen(mpiexec, shell=True, stdout=PIPE, stderr=PIPE)
                    stdout, stderr = process.communicate()
                    self.exec_results[test.name] = [stdout.decode('UTF-8'),
                                                    stderr.decode('UTF-8')]
                    test.exec_results = [stdout.decode('UTF-8'),
                                        stderr.decode('UTF-8')]

                    # Determines if a test passes or fails and stores result internally
                    test.exec_result_parser()
        else:
            # If specific list isn't defined, all exectuables are run
            # DEPRECATED
            # This behavior works currently for compatability
            files = pathlib.Path(self.test_directory).glob('**/*.c')
            for test in files:
                test_name = str(test)[len(self._test_directory)+1: len(str(test))-2]
                mpiexec = ["mpiexec"] + args + [self.test_directory + test_name]
                process = Popen(mpiexec, shell=True, stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()
                self.exec_results[test_name] = [stdout.decode('UTF-8'),
                                                stderr.decode('UTF-8')]

        return self.exec_results
