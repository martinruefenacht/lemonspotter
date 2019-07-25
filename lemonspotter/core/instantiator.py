from typing import Generator

from core.variable import Variable
from core.parameter import Parameter

class Instantiator:
    def __init__(self):
        pass

    def generate_variable(self, parameter: Parameter) -> Generator[Variable, None, None]:
        pass

