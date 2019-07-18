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

        self.properties = {}

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

    @property
    def name(self):
        return self._name
    
    @property
    def abstract_type(self):
        return self._abstract_type

    @property
    def validated(self):
        return self._validated

    @validated.setter
    def validated(self, validated):
        self._validated = validated

    @validated.deleter
    def validated(self):
        del self._validated

    @property
    def attempted(self):
        return self._attempted

    @attempted.setter
    def attempted(self, attempted):
        self._attempted = attempted

    @attempted.deleter
    def attempted(self):
        del self._attempted

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
