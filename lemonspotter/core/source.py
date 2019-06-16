class Source:
    def __init__(self, name: str):
        self._name = name

        self._front_lines = []
        self._back_lines = []

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
