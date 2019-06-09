import os

class Source:
    def __init__(self, name):
        self._name = name

        self.source_lines = []

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        del self._name

    def write(self):
        if not os.path.isdir('../tests'):
            os.makedirs("../tests")

        file_name = self.name + ".c"
        test_file = open("../tests/" + file_name, "w+")

        for line in self.source_lines:
            test_file.write(line+"\n")

        test_file.close()
