"""Defines a type object of from library that can be included in Lemonspotter tests."""

class Type:
    """
    Defines a type object of from library that can be included in Lemonspotter tests.
    """
    def __init__(self, abstract_type, source, ctype, range=[], name="CONSTANT_UNDEFINED", default=''):
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
        self._abstract_type = abstract_type
        self._ctype = ctype
        self._source = source
        self._range = range
        self._validation = False
        self._default = default

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
    
    @property
    def default(self):
        return self._default

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
    def abstract_type(self):
        return self._abstract_type

    @property
    def language_type(self):
        return self._ctype

    @property
    def lower_range(self):
        return self._range[0]

    @lower_range.setter
    def lower_range(self, lower_range):
        self._range[0] = lower_range

    @property
    def upper_range(self):
        return self._range[1]

    @lower_range.setter
    def upper_range(self, upper_range):
        self._range[1] = upper_range

    @property
    def validation(self):
        return self._validation

    @validation.setter
    def validation(self, validation):
        self._validation = validation

    @validation.deleter
    def validation(self):
        del self.validation
