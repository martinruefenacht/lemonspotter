import os
import pathlib
from subprocess import Popen, PIPE

class MPIExecutor:
    def __init__(self, test_directory='../tests/'):
        """
        Initializes a test executor for MPI Libraries
        """

        self._test_directory = os.path.abspath(test_directory)
        self._build_results = {}
        self._exec_results = {}

    @property
    def build_results(self):
        """
        Returns build_results of a test
        """

        return self._build_results

    @build_results.setter
    def build_results(self, build_results):
        """
        Sets the build_results of a test
        """

        self._build_results = build_results

    @build_results.deleter
    def build_results(self):
        """
        Delets the build_results of a test
        """
        del self._build_results

    @property
    def exec_results(self):
        """
        Returns exec_results of a test
        """
        return self._exec_results

    @exec_results.setter
    def exec_results(self, exec_results):
        """
        Sets the exec_results of a test
        """
        self._exec_results = exec_results

    @exec_results.deleter
    def exec_results(self):
        """
        Delets the exec_results of a test
        """
        del self._exec_results

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

    def build(self, tests, args=[]):
        """
        Builds a test into a runnable executable

        tests: list of test objects that define the tests to run
        """

        if not os.path.isdir(self.test_directory):
            os.makedirs(self.test_directory)

        if tests:
            for test in tests:
                # Generate MPICC command that compiles test excutable
                file_name = test.name + ".c"
                mpicc = ["mpicc", file_name] + args + ["-o", self.test_directory, test.name]

                process = Popen(mpicc, shell=True, stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()

                self.build_results[test.name] = [stdout.decode('UTF-8'),
                                                 stderr.decode('UTF-8')]
                test.build_results = [stdout.decode('UTF-8'),
                                      stderr.decode('UTF-8')]

                # Determines if a test passes or fails and stores result internally
                test.build_result_parser()

        else:
            # DEPRECATED
            # This behavior works currently for compatability.
            files = pathlib.Path(self.test_directory).glob('**/*.c')
            for test in files:
                test_name = str(test)[len(self._test_directory): len(str(test))-2]
                # Generate MPICC command that compiles test excutable
                mpicc = ["mpicc", str(test)] + args + ["-o", self.test_directory, test_name]

                process = Popen(mpicc, shell=True, stdout=PIPE, stderr=PIPE)
                self.build_results[test_name] = [str(stdout).decode('UTF-8'),
                                                 str(stderr).decode('UTF-8')]

        return self.build_results

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
