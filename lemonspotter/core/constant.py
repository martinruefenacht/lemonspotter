"""Defines a constant of a library that can be included in Lemonspotter tests."""

class Constant:
    """
    Defines an element of a library that can be included in Lemonspotter tests.
    """
    def __init__(self, abstract_type, name="CONSTANT_UNDEFINED", validated=False):
        """
        Initializes object of class Constant.

        Parameters:
        name           (string)    : Name of the constant
        classification (string)    : Coorespondes to what this element is supposed to return
        validation     (boolean)   : Determines whether the constant has been validated
        """
        self.name = name
        self.abstract_type = abstract_type
        self.validated = validated

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_name(self):
        """
        Gets the name of the constant
        """
        return self.name

    def get_abstract_type(self):
        """
        Gets the abstract_type(type) of the constant
        """
        return self.abstract_type

    def get_validation(self):
        """
        Gets the validation status for the constant
        """
        return self.validated

    def set_name(self, name):
        """
        Sets the name of the constant
        """
        self.name = name

    def set_abstract_type(self, abstract_type):
        """
        Sets the abstract_type(type) of the constant
        """
        self.abstract_type = abstract_type

    def set_validation(self, validated):
        """
        Sets the validation status for the constant
        """
        self.validated = validated
