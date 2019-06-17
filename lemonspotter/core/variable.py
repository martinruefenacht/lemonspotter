"""
This module defines the Variable class.
"""

class Variable:
    """
    This class represents any C variable for source code generation.
    """

    def __init__(self, kind: str, name: str, pointer_level: int = 0) -> None:
        """
        This method constructs the Variable from a type, name and pointer level.
        """

        self.kind = kind
        self.name = name
        self.pointer_level = pointer_level

    def generate_print_statement(self) -> str:
        """
        Generates a C printf statement for this variable.
        """

        # hard coded mapping between printf format and C type
        if self.kind.ctype == 'int':
            # TODO this is a function call statement
            # we don't care about return variable though
            return 'printf("' + self.name + ' %i\\n", ' + self.name + ');'

        raise NotImplementedError

    def generate_check_statement(self) -> str:
        """
        Generates a C statement to check if the variable is valid.
        """

        if self.kind.abstract_type == 'ERRORCODE':
            # TODO this is an if statement
            return 'if(' + self.name + ' != MPI_SUCCESS) exit(0);'

        raise NotImplementedError
