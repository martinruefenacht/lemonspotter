class Database:
    def __init__(self):
        self.functions = set()
        self.constants = set()
        self.types     = set()

        self.functions_by_name = {}
        self.constants_by_abstract_type = {}
        self.types_by_abstract_type = {}

    def add_constant(self, constant):
        # add to set of constants
        self.constants.add(constant)

        # add to lookup
        if constant.get_abstract_type() not in self.constants_by_abstract_type:
            self.constants_by_abstract_type[constant.get_abstract_type()] = []

        self.constants_by_abstract_type[constant.get_abstract_type()].append(constant)

    def add_function(self, function):
        # add to set of functions
        self.functions.add(function)
        
        # add to function lookup
        self.functions_by_name[function.name] = function 

    def add_type(self, type_obj):
        # add to set of types
        self.types.add(type_obj)

        # add to dictionary of types
        self.types_by_abstract_type[type_obj.abstract_type] = type_obj
