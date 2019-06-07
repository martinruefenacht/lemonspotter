import os
import pathlib
import json

from core.database import Database
from core.function import Function
from core.type     import Type

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
        print(database.functions)

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
                
                func_name = func['name']
                func_return = func['return']
                func_parameters = func['parameters'] 
                func_needs_any = func['needs_any']
                func_needs_all = func['needs_all']
                func_leads_any = func['leads_any']
                func_leads_all = func['leads_all']

                func_obj = Function(func_name, 
                                        func_return,
                                        func_parameters,
                                        func_needs_any,
                                        func_needs_all,
                                        func_leads_any,
                                        func_leads_all)

                database.functions[func_name] = func_obj

    def parse_single_function(self, path):
        with open(path) as funcfile:
            return json.load(funcfile)

    def parse_errors(self, path, database):
        raise NotImplementedError

    def parse_single_error(self):
        raise NotImplementedError 
        

    def parse_types(self, path, database):
        # load defaults
        with open(path + 'defaults.json') as default_file:
            defaults = json.load(default_file)

        # load single file definitions
        types_filename = path + 'types.json'
        if os.path.isfile(types_filename):
            with open(types_filename) as types_file:
                type_array = json.load(types_file)

                for mpi_type in type_array:

                    type_name = mpi_type['name']
                    type_classification = mpi_type['abstract_type']
                    
                    type_source = mpi_type['source']
                    for source in type_source:
                        if source == "range":   
                            type_lower_range = mpi_type['range'][0]
                            type_upper_range = mpi_type['range'][1]

                    type_obj = Type(type_classification,
                                    type_source,
                                    [type_lower_range, type_upper_range], 
                                    type_name)

                    database.types[mpi_type['name']] = type_obj
        
        # load directory definitions
        types_directory = path + 'types/'
        if os.path.isdir(types_directory):
            files = pathlib.Path(types_directory).glob('**/*.json')

            for path in files:
                mpi_type = self.parse_single_type(path)
                
                type_name = mpi_type['name']
                type_classification = mpi_type['abstract_type']
                
                type_source = mpi_type['source']
                for source in type_source:
                    if source == "range":   
                        type_lower_range = mpi_type['range'][0]
                        type_upper_range = mpi_type['range'][1]

                type_obj = Type(type_classification,
                                type_source,
                                [type_lower_range, type_upper_range], 
                                type_name)

                database.types[mpi_type['name']] = type_obj





    def parse_single_type(self, path):
        with open(path) as typefile:
            return json.loads(typefile)
