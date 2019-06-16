import os

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
        Adds a generated string to the fron of the source code.
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

    def write(self):
        """
        Writes source object to file that can be compiled/run 
        by executors.
        """
        if not os.path.isdir('../tests'):
            os.makedirs("../tests")

        file_name = self.name + ".c"
        test_file = open("../tests/" + file_name, "w+")

        for line in self.source_lines:
            test_file.write(line+"\n")

        test_file.close()
