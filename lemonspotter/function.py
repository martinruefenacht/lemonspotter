"""Defines a function of a library that can be included in Lemonspotter tests."""

class Function:
    """
    Defines an element of a library that can be included in Lemonspotter tests.
    """

    def __init__(self, name="FUNCTION_NOT_FOUND", return_type="", arguments=[], requires=[], start=False, end=False, validated=False):
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
        self.arguments = arguments
        self.return_type = return_type
        self.requires = requires
        self.start = start
        self.end = end
        self.validated = validated


    def get_name(self):
        """
	    Returns the name of the element.
        """
        return self.function_name

    def get_arguments_list(self):
        """
        Returns the list of arguments that an element takes.
        """
        return self.arguments

    def get_return_type(self):
        """
        Returns the return type of the element.
        """
        return self.return_type

    def get_dependency_list(self):
        """
        Returns the dependency list for an element.
        """
        return self.requires

    def get_start(self):
        """
        Returns boolean value if element is start point
        """
        return self.start

    def get_end(self):
        """
        Returns boolean value if element is end point
        """
        return self.end

    def set_validation(self, validation):
        """
        Sets the validation state after testing
        """
        self.validated = validation

    def get_validation(self):
        """
        Returns validation state of each element
        """
        return self.validated