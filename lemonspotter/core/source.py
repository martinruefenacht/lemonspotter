from core.statement import Statement, BlockStatement
from core.variable import Variable

class Source:
    def __init__(self, name: str):
        self._name = name
        self._sources = sources

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
