"""Defines a constant of a library that can be included in Lemonspotter tests."""

class Constant:
    """
    Defines an element of a library that can be included in Lemonspotter tests.
    """
    def __init__(self, classification, name="CONSTANT_UNDEFINED", validated=False):
        """
        Initializes object of class Constant.

        Parameters:
        name           (string)    : Name of the constant
        classification (string)    : Coorespondes to what this element is supposed to return
        validation     (boolean)   : Determines whether the constant has been validated
        """
        self.name = name
        self.classification = classification
        self.validated = validated

    def get_name(self):
        """
        Gets the name of the constant
        """
        return self.name

    def get_classification(self):
        """
        Gets the classification(type) of the constant
        """
        return self.classification

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

    def set_classification(self, classification):
        """
        Sets the classification(type) of the constant
        """
        self.classification = classification

    def set_validation(self, validated):
        """
        Sets the validation status for the constant
        """
        self.validated = validated
