"""
This module defines the Variable class which represents Variables and their values in
Source classes.
"""

from typing import Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from core.type import Type


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

        self._pointer_level: int = 0

    @property
    def type(self) -> 'Type':
        """This property provides the Type object of the Variable."""

        return self._type

    @property
    def name(self) -> str:
        """This property provides the name of the Variable."""

        assert self._name is not None
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """"""

        assert name is not None
        self._name = name

    @property
    def value(self) -> Optional[str]:
        """This property provides the value of the Variable."""

        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """This allows setting the value of the Variable."""

        assert value is not None
        self._value = value

    @property
    def predefined(self) -> bool:
        """"""

        return self._predefined

    @property
    def pointer_level(self) -> int:
        return self._pointer_level
    
    @pointer_level.setter
    def pointer_level(self, level: int) -> None:
        """"""

        assert level is not None
        assert level >= 0

        self._pointer_level = level

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
