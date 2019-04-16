"""Defines an element of a library that can be included in Lemonspotter tests."""

class Element:
    """
    Defines an element of a library that can be included in Lemonspotter tests.
    """

    def __init__(self, name="ELEMENT_NOT_FOUND", return_type="", arguments=[], requires=[], start=False, end=False, validated=False):
        """
        Initializes object of class Element.

        Parameters:
        name        (string)    : Name of the element
        return_type (string)    : Coorespondes to what this element is supposed to return
        arguments   (string[])  : List of items that this function takes as a parameter
        requires    (string[])  : List of element names that current element needs to run
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

    def get_validation(self):
        """
        Returns validation state of each element
        """
        return self.validated