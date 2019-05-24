"""Defines a error code of a library that can be included in Lemonspotter tests."""

class Error:
    """
    Defines a constant of a library that can be included in Lemonspotter tests.
    """
    def __init__(self, value, symbol="ERROR_UNDEFINED", validated=False):
        """
        Initializes object of class Element.

        Parameters:
        name        (string)    : Name of the element
        return_type (string)    : Coorespondes to what this element is supposed to return
        arguments   (string[])  : List of items that this function takes as a parameter
        requires    (string[])  : List of element names that current element needs to run
        """
        self.symbol = symbol
        self.value = value
        self.validated = validated

    def get_symbol(self):
        """
        Gets the symbol of the constant
        """
        return self.symbol

    def get_value(self):
        """
        Gets the value of the constant
        """
        return self.value

    def get_validation(self):
        """
        Gets the validation status for the error
        """
        return self.validated

    def set_symbol(self, symbol):
        """
        Sets the symbol of the constant
        """
        self.symbol = symbol

    def set_value(self, value):
        """
        Sets the value of the constant
        """
        self.value = value

    def set_validation(self, validated):
        """
        Sets the validation status for the error
        """
        self.validated = validated
