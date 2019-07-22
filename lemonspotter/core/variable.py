"""
This module defines the Variable class.
"""

from typing import Optional
import logging

from core.type import Type

class Variable:
    """
    This class represents any C variable for source code generation.
    """

    def __init__(self, kind: Type, name: str, value: str=None, pointer_level: int = 0) -> None:
        """
        This method constructs the Variable from a type, name and pointer level.
        """

        self._type: Type = kind
        self._name: str = name
        self._value: Optional[str] = value
        self._pointer_level: int = pointer_level
        
    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self._name

    @property
    def kind(self) -> Type:
        return self._type

    @property
    def type(self) -> Type:
        return self._type

    @property
    def name(self) -> str:
        return self._name

    @property
    def pointer_level(self) -> int:
        return self._pointer_level

    @property
    def value(self) -> Optional[str]:
        return self._value
    @value.setter
    def value(self, value: str) -> None:
        self._value = value
