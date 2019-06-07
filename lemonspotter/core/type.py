"""Defines a type of a library that can be included in Lemonspotter tests."""

class Type:
    """
    Defines an element of a library that can be included in Lemonspotter tests.
    """
    def __init__(self, classification, source, ctype, range=[], name="CONSTANT_UNDEFINED", placeholder="UNDEFINED"):
        """
        Initializes object of class Constant.

        Parameters:
        name           (string)    : Name of the type
        classification (string)    : Coorespondes to what this type is classified as
        validation     (boolean)   : Determines whether the type has been validated
        """
        self.name = name
        self.placeholder = placeholder
        self.classification = classification
        self.ctype = ctype 
        self.source = source
        self.range = range
        self.validated = False

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def get_name(self):
        """
        Gets the name of the type
        """
        return self.name

    def get_placeholder(self):
        """
        Gets the placeholder of the type
        """
        return self.placeholder

    def get_classification(self):
        """
        Gets the classification(type) of the type
        """
        return self.classification

    def get_lower_range(self):
        """
        Gets the lower range of the constant
        """
        return self.range[0]

    def get_upper_range(self):
        """
        Gets the upper range of the constant
        """
        return self.range[1]

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

    def set_placeholder(self, placeholder):
        """
        Sets the placeholder of the constant
        """
        self.placeholder = placeholder

    def set_classification(self, classification):
        """
        Sets the classification(type) of the constant
        """
        self.classification = classification

    def set_lower_range(self, lower_range):
        """
        Sets the lower range of the constant
        """
        self.range[0] = lower_range

    def set_upper_range(self, upper_range):
        """
        Sets the upper range of the constant
        """
        self.range[1] = upper_range

    def set_validation(self, validated):
        """
        Sets the validation status for the constant
        """
        self.validated = validated
