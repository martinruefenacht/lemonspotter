"""Defines a function of a library that can be included in Lemonspotter tests."""

class Function:
    """
    Defines an element of a library that can be included in Lemonspotter tests.
    """

    #def __init__(self, name="FUNCTION_NOT_FOUND", return_type="", arguments=[], requires=[], start=False, end=False, validated=False):
    def __init__(self, name, return_type, parameters, needs_any, needs_all, leads_any, leads_all):
        """
        Initializes function element.

        Parameters:
        name        (string)    : Name of the function
        return_type (string)    : Coorespondes to what this function is supposed to return
        arguments   (string[])  : List of items that this function takes as a parameter
        requires    (string[])  : List of element names that current function needs to run
        validation  (boolean)   : Determines whether the constant has been validated
        """
        self.function_name = name
        self.parameters = parameters
        self.return_type = return_type

        #self.requires = requires
        #self.start = start
        #self.end = end

        self._needs_any = needs_any
        self._needs_all = needs_all

        self._leads_any = leads_any
        self._leads_all = leads_all

        self._attempted = False
        self._validated = False

    def is_attempted(self):
        return self._attempted

    def is_validated(self):
        return self._validated

    def has_failed(self):
        return self._attempted and not self._validated

    def validate(self):
        self._validated = True

    def attempt(self):
        self._attempted = True

    def __repr__(self):
        return self.function_name

    def __str__(self):
        return self.function_name
