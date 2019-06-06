class MPIParser:
    def __init__(self, database_path):
        self.database_path = database_path

    def parse_constants(self):
        raise NotImplementedError
       
    def parse_single_constant(self):
        raise NotImplementedError 

    def parse_functions(self):
        raise NotImplementedError

    def parse_single_function(self):
        raise NotImplementedError

    def parse_errors(self):
        raise NotImplementedError

    def parse_single_error(self):
        raise NotImplementedError

    def parse_types(self):
        raise NotImplementedError

    def parse_single_type(self):
        raise NotImplementedError
