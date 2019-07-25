"""
This module defines the Variable class which represents Variables and their values in
Source classes.
"""

from typing import Optional

from core.type import Type


class Variable:
    """
    This class represents any C variable for source code generation.
    """

    def __init__(self, kind: Type, name: str = None, value: str = None, pointer_level: int = 0) -> None:
        """
        This method constructs the Variable from a type, name and pointer level.
        """

        self._type: Type = kind
        self._name: Optional[str] = name
        self._value: Optional[str] = value
        self._pointer_level: int = pointer_level

    def __str__(self) -> str:
        assert self._name is not None
        return self._name

    def __repr__(self) -> str:
        assert self._name is not None
        return self._name

    @property
    def type(self) -> Type:
        """This property provides the Type object of the Variable."""

        return self._type

    @type.setter
    def type(self, kind: Type) -> None:
        """"""

        self._type = kind

    @property
    def name(self) -> str:
        """This property provides the name of the Variable."""

        assert self._name is not None
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """"""

        self._name = name

    @property
    def pointer_level(self) -> int:
        """This property provides the pointer level of this Variable."""

        return self._pointer_level

    @pointer_level.setter
    def pointer_level(self, level: int) -> None:
        """"""

        self._pointer_level = level

    @property
    def value(self) -> Optional[str]:
        """This property provides the value of the Variable."""

        return self._value

    @value.setter
    def value(self, value: str) -> None:
        """This allows setting the value of the Variable."""

        self._value = value
