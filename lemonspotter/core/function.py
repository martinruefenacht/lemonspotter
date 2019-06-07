"""    Defines an function object that can be included in Lemonspotter tests."""

class Function:
    """
    Defines an function object that can be included in Lemonspotter tests.
    """

    def __init__(self, name, return_type, arguments, needs_any, needs_all, leads_any, leads_all):
        """
        Initializes function element.

        Parameters:
        name        (string)    : Name of the function
        return_type (string)    : Coorespondes to what this function is supposed to return
        arguments   (string[])  : List of items that this function takes as a parameter
        needs_any   (string[])  : TODO
        needs_all   (string[])  : TODO
        leads_any   (string[])  : TODO
        leads_all   (string[])  : TODO
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

    def __repr__(self):
        """
        Defines informal string behavior for function type
        """
        return self.function_name

    def __str__(self):
        """
        Defines formal string behavior for function type
        """
        return self.function_name

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

    
