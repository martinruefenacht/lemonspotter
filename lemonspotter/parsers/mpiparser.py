import os
import pathlib
import json

from core.database import Database

class MPIParser:
#    def __call__(self, database_path: str) -> Database:
    def __call__(self, database_path):
        self.parse(database_path)
        
#    def parse(self, database_path: str) -> Database:
    def parse(self, path):
        database = Database()

        self.parse_types(path, database)
        #self.parse_errors(path, database)
        #self.parse_constants(path, database)
        self.parse_functions(path, database)

        #print(database.types)
        #print(database.functions)

        # TODO generate objects

        return database

    def parse_constants(self, path):
        raise NotImplementedError 
       
    def parse_single_constant(self):
        raise NotImplementedError 

    def default_function(self, func, defaults):
        # default function level
        for key in defaults['function'].keys():
            if key not in func:
                func[key] = defaults['function'][key] 
        
        # default parameter level
        for parameter in func['parameters']:
            for key in defaults['parameter'].keys():
                if key not in parameter:
                    parameter[key] = defaults['parameter'][key]

    def parse_functions(self, path, database):
        # load defaults
        with open(path + 'defaults.json') as default_file:
            defaults = json.load(default_file)

        # load single file
        # TODO

        # load directory function definitions
        functions_directory = path + 'functions/'
        if os.path.isdir(functions_directory):
            files = pathlib.Path(functions_directory).glob('**/*.json')

            for path in files:
                func = self.parse_single_function(path.absolute())

                self.default_function(func, defaults)
                
                database.functions[func['name']] = func

    def parse_single_function(self, path):
        with open(path) as funcfile:
            return json.load(funcfile)

    def parse_errors(self, path, database):
        raise NotImplementedError

    def parse_single_error(self):
        raise NotImplementedError

    def parse_types(self, path, database):
        # load single file definitions
        types_filename = path + 'types.json'
        if os.path.isfile(types_filename):
            with open(types_filename) as types_file:
                type_array = json.load(types_file)

                for mpi_type in type_array:
                    database.types[mpi_type['name']] = mpi_type
        
        # load directory definitions
        types_directory = path + 'types/'
        if os.path.isdir(types_directory):
            files = pathlib.Path(types_directory).glob('**/*.json')

            for path in files:
                mpi_type = self.parse_single_type(path)
                database.types[mpi_type['abstract_type']] = mpi_type

    def parse_single_type(self, path):
        with open(path) as typefile:
            return json.loads(typefile)
