"""
This module defines the Variable class which represents Variables and their values in
Source classes.
"""

from typing import Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from lemonspotter.core.type import Type


class Variable:
    """
    This class represents any C variable for source code generation.
    """

    def __init__(self,
                 kind: 'Type',
                 name: str = None,
                 value: str = None,
                 predefined: bool = False) -> None:
        """
        This method constructs the Variable from a type, name and pointer level.
        """

        self._type: 'Type' = kind
        self._name: Optional[str] = name
        self._value: Optional[str] = value
        self._predefined: bool = predefined

    @property
    def type(self) -> 'Type':
        """This property provides the Type object of the Variable."""

        return self._type

    @property
    def name(self) -> str:
        """This property provides the name of the Variable."""

        if self._name is None:
            raise Exception('Name is None.')

        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """"""

        if name is None:
            raise Exception('Assigning None to name of Variable.')

        self._name = name

    @property
    def value(self) -> Optional[str]:
        """This property provides the value of the Variable."""

        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """This allows setting the value of the Variable."""

        if value is None:
            raise Exception('Assigning None to value of Variable.')

        self._value = value

    @property
    def predefined(self) -> bool:
        """"""

        return self._predefined

    def validate(self) -> bool:
        """
        Test whether the value of this variable is a valid value according to the
        variable type.
        """

        if self.value is None:
            raise RuntimeError(('Attempting to validate variable %s against specification'
                                ' with None value.', self.name))

        logging.debug('validating variable %s', self.name)

        # validate against type spec
        return self.type.validate(self.value)
