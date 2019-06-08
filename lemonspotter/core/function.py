"""    Defines an function object that can be included in Lemonspotter tests."""

from typing import List

from core.variable import Variable

class Function:
    """
    Defines an function object that can be included in Lemonspotter tests.
    """

    def __init__(self, name, return_type, parameters, needs_any, needs_all, leads_any, leads_all):
        """
        Initializes function element.

        Parameters:
        name         (string)    : Name of the function
        return_type  (string)    : Coorespondes to what this function is supposed to return
        parameters   (string[])  : List of items that this function takes as a parameter
        needs_any    (string[])  : TODO
        needs_all    (string[])  : TODO
        leads_any    (string[])  : TODO
        leads_all    (string[])  : TODO
        """

        self._name = name
        self._parameters = parameters
        self._return_type = return_type

        self._needs_any = needs_any
        self._needs_all = needs_all

        self._leads_any = leads_any
        self._leads_all = leads_all

        self._attempted = False
        self._validated = False

    def __repr__(self) -> str:
        """
        Defines informal string behavior for function type
        """
        return self._name

    def __str__(self) -> str:
        """
        Defines formal string behavior for function type
        """
        return self._name

    def generate_function_expression(self, variables: List[Variable]) -> str:
        raise NotImplementedError

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        del self._name

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = parameters

    @parameters.deleter
    def parameters(self):
        del self._parameters
    
    @property
    def return_type(self):
        return self._return_type
    
    @return_type.setter
    def return_type(self, return_type):
        self._return_type = return_type

    @return_type.deleter
    def return_type(self):
        del self._return_type

    @property
    def needs_any(self):
        return self._needs_any
    
    @needs_any.setter
    def needs_any(self, needs_any):
        self._needs_any = needs_any

    @needs_any.deleter
    def needs_any(self):
        del self._needs_any

    @property
    def needs_all(self):
        return self._needs_all
    
    @needs_all.setter
    def needs_all(self, needs_all):
        self._needs_all = needs_all

    @needs_all.deleter
    def needs_all(self):
        del self._needs_all

    @property
    def leads_any(self):
        return self._leads_any
    
    @leads_any.setter
    def leads_any(self, leads_any):
        self._leads_any = leads_any

    @leads_any.deleter
    def leads_any(self):
        del self._leads_any

    @property
    def leads_all(self):
        return self._leads_all
    
    @leads_all.setter
    def leads_all(self, leads_all):
        self._leads_all = leads_all

    @leads_all.deleter
    def leads_all(self):
        del self._leads_all

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

    
