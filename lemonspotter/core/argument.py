"""
This module contains the class definition of an Argument.
"""

from typing import Sequence, Optional

from lemonspotter.core.variable import Variable


class Argument:
    """
    This class represents parameters of Function objects translated from the specification.
    """

    # TODO Arguments need to also support code fragements?
    # some dependencies will require executing additional code.

    def __init__(self,
                 variable: Variable,
                 variables: Optional[Sequence[Variable]] = None):
        self._variable = variable
        self._variables = variables

    @property
    def variable(self) -> Variable:
        """
        """

        return self._variable

    @property
    def has_dependencies(self) -> bool:
        """
        """

        return self._variables is not None

    @property
    def dependencies(self) -> Sequence[Variable]:
        """
        """

        if self._variables is None:
            raise RuntimeError('No dependencies for this argument.')

        return self._variables
