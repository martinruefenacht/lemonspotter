"""Defines a type object of from library that can be included in Lemonspotter tests."""

class Type:
    """
    Defines a type object of from library that can be included in Lemonspotter tests.
    """
    def __init__(self, abstract_type, source, ctype, range=[], name="CONSTANT_UNDEFINED"):
        """
        Initializes object of class Type.

        Parameters:
        abstract_type  (string)    : Coorespondes to what this type is classified as
        source         (list)      : Holds information about type
        ctype          (string)    : Holds the c-style datatype of the type
        range          (list)      : Holds lower & upper bounds of type 
        name           (string)    : Name of the type
        """
        self._name = name
        self.abstract_type = abstract_type
        self._ctype = ctype 
        self.source = source
        self.range = range
        self.validated = False

    def __str__(self):
        """
        Defines formal string represenation of Type
        """
        return self._name
    
    def __repr__(self):
        """
        Defines informal string represenation of Type
        """
        return self._name

    def get_name(self):
        """
        Gets the name of the type
        """
        return self._name

    def get_abstract_type(self):
        """
        Gets the abstract_type of the type
        """
        return self._abstract_type

    def get_ctype(self):
        """
        Gets the cstyle type for a variable
        """
        return self._ctype

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
        self._name = name

    def set_abstract_type(self, abstract_type):
        """
        Sets the abstract_type of the constant
        """
        self._abstract_type = abstract_type

    def set_ctype(self, ctype):
        """
        Sets the ctype for type
        """
        self._ctype = ctype

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
