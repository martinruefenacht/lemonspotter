import os

class Test:
    def __init__(self, name: str, sources=[], expected_result='pass'):
        self._name = name
        self._sources = sources

        self._build_results = []
        self._exec_results = []

        # Outcome can be pass/fail/xfail/xpass
        self._expected_result = expected_result

        # Actual outcome after tested.
        # Until set default value is ''
        # Once tested can be set to pass/fail/xfail/xpass
        self._result = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        del self._name

    @property
    def sources(self):
        return self._sources

    @sources.setter
    def sources(self, sources):
        self._sources = sources

    @sources.deleter
    def sources(self):
        del self._sources

    @property
    def build_results(self):
        return self._build_results

    @build_results.setter
    def build_results(self, build_results):
        self._build_results = build_results

    @build_results.deleter
    def build_results(self):
        del self._build_results

    @property
    def exec_results(self):
        return self._exec_results

    @exec_results.setter
    def exec_results(self, exec_results):
        self._exec_results = exec_results

    @exec_results.deleter
    def exec_results(self):
        del self._exec_results

    @property
    def expected_result(self):
        return self._expected_result

    @expected_result.setter
    def expected_result(self, expected_result):
        self._expected_result = expected_result

    @expected_result.deleter
    def expected_result(self):
        del self._expected_result

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = result

    @result.deleter
    def result(self):
        del self._result



    def write(self):
        """
        Writes source object to file that can be compiled/run
        by executors.
        """
        if not os.path.isdir('../tests'):
            os.makedirs("../tests")

        file_name = self.name + ".c"
        test_file = open("../tests/" + file_name, "w+")

        for source in self.sources:
            test_file.write(source.get_source())

        test_file.close()

    def build_result_parser(self):
        """
        Fails test if build process produces error
        """
        if self.build_results[1]:
            print("BUILD ERROR: " + self.name + " failed to build.")
            self.result = "failed"

    def exec_result_parser(self):
        """
        Parses output of test execution into results
        """
        if self.expected_result == 'pass':
            if self.exec_results[1]:
                print("STDERR Not Empty")
                print(self.exec_results[1])


class Source:
    def __init__(self, name: str):
        self._name = name
        self._front_lines = []
        self._back_lines = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        del self._name

    def add_at_start(self, line: str) -> None:
        """
        Adds a generated string to the front of the source code.
        """

        self._front_lines.append(line)

    def add_at_end(self, line: str) -> None:
        """
        Adds a generated string to the back of the source code.
        """

        self._back_lines.append(line)

    def get_source(self) -> str:
        """
        Combines the front and back lines into a single string.
        """

        lines = '\n'.join(self._front_lines) + '\n'
        lines = lines + '\n'.join(self._back_lines)

        return lines
