import os

class Test:
    def __init__(self, name: str, sources=[], expected_outcome='pass'):
        self._name = name
        self._sources = sources
        self._results = []
        self._expected_outcome = expected_outcome

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
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        self._results = results

    @results.deleter
    def results(self):
        del self._results

    @property
    def expected_outcome(self):
        return self._expected_outcome

    @expected_outcome.setter
    def expected_outcome(self, expected_outcome):
        self._expected_outcome = expected_outcome

    @expected_outcome.deleter
    def expected_outcome(self):
        del self._expected_outcome


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
