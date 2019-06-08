"""Defines an constant that can be included in Lemonspotter tests."""

class Constant:
    """
    Defines an constant that can be included in Lemonspotter tests.
    """
    def __init__(self, abstract_type, name="CONSTANT_UNDEFINED"):
        """
        Initializes object of class Constant.

        Parameters:
        abstract_type  (string)    : Underlying type of constant
        name           (string)    : Name of the constant
        """

        self._name = name
        self._abstract_type = abstract_type
        self._attempted = False
        self._validated = False

    def __repr__(self):
        """
        Defines informal string behavior for constant class
        """
        return self._name

    def __str__(self):
        """
        Defines formal string behavior for constant class
        """
        return self._name

    def get_name(self):
        """
        Gets the name of the constant
        """
        return self._name

    def set_name(self, name):
        """
        Sets the name of the constant
        """
        self.name = _name

    def get_abstract_type(self):
        """
        Gets the abstract_type(type) of the constant
        """
        return self._abstract_type

    def set_abstract_type(self, abstract_type):
        """
        Sets the abstract_type(type) of the constant
        """
        self._abstract_type = abstract_type

    def is_attempted(self):
        """
        Sets attempted variable
        """
        return self._attempted

    def is_validated(self):
        """
        Sets validated variable
        """
        return self._validated

    def has_failed(self):
        """
        Deterministic test to determine if function has failed tests
        """
        return self._attempted and not self._validated

    def validate(self):
        """
        Sets the validation state of the function to true
        """
        self._validated = True

    def invalidate(self):
        """
        Sets the validation state of the function to false
        """
        self._validated = True

    def attempt(self):
        """
        Sets the attempt state of the function
        """
        self._attempted = True
