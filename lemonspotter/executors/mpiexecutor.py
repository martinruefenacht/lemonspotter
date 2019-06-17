import os
import pathlib
from subprocess import Popen, PIPE

class MPIExecutor:
    def __init__(self, test_directory='../tests/'):
        self._test_directory = test_directory
        self._results = {}

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        self._results = results

    @results.deleter
    def results(self):
        del self._results

    @property
    def test_directory(self):
        return self._test_directory

    @test_directory.setter
    def test_directory(self, test_directory):
        self._test_directory = test_directory

    @test_directory.deleter
    def test_directory(self):
        del self._test_directory

    def build(self):
        if not os.path.isdir(self.test_directory):
            os.makedirs(test_directory)

        files = pathlib.Path(self.test_directory).glob('**/*.c')

        for test in files:
            test_name = str(test)[len(self._test_directory): len(str(test))-2]
            mpicc = "mpicc " + str(test) + " -o " + self.test_directory + test_name
            process = Popen(mpicc, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()

    def run(self):

        if not os.path.isdir(self.test_directory):
            os.makedirs(test_directory)
        files = pathlib.Path(self.test_directory).glob('**/*.c')
        for test in files:
            test_name = str(test)[len(self._test_directory): len(str(test))-2]
            mpiexec = "mpiexec " + self.test_directory + test_name
            process = Popen(mpiexec, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            self.results[test_name] =  [str(stdout), str(stderr)]


        return self.results