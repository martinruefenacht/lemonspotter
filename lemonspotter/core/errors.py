"""Defines a error code of a library that can be included in Lemonspotter tests."""

class Error:
    """
    Defines a constant of a library that can be included in Lemonspotter tests.
    """
    def __init__(self, value, symbol="ERROR_UNDEFINED"):
        """
        Initializes object of class Element.

        Parameters:
        name        (string)    : Name of the element
        return_type (string)    : Coorespondes to what this element is supposed to return
        arguments   (string[])  : List of items that this function takes as a parameter
        requires    (string[])  : List of element names that current element needs to run
        """
        self._symbol = symbol
        self._value = value
        self._validated = False

    def __str__(self):
        return self._symbol

    def __repr__(self):
        return self._symbol

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol

    @symbol.deleter
    def symbol(self, symbol):
        del self._symbol

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

    @value.deleter
    def value(self, value):
        del self._value

    @property
    def validated(self):
        return self._validated
    
    @validated.setter
    def validated(self, validated):
        self._validated = validated

    @validated.deleter
    def validated(self):
        del validated