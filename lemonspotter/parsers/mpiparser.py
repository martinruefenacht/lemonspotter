from pathlib import Path
import json
from typing import Dict, Any
import os

from core.database import Database
from core.function import Function
from core.type     import Type
from core.constant import Constant

class MPIParser:
    def __call__(self, database_path: Path) -> Database:
        return self.parse(database_path)
        
    def parse(self, database_path: Path) -> Database:
        database = Database()

        self.parse_types(database_path, database)
        self.parse_constants(database_path, database)
        self.parse_functions(database_path, database)

        return database

    def parse_constants(self, path: Path, database: Database) -> None:
        # parse single file
        constants_filename = path / 'constants.json'

        if constants_filename.exists():
            with constants_filename.open() as constants_file:
                constants_array = json.load(constants_file)
                
                for constant in constants_array:
                    database.add_constant(Constant(database, constant))

        # TODO parse subdirectory of constants
#        constants_directory = path + 'constants/'
#        if os.path.isdir(constants_directory):
#            files = pathlib.Path(types_directory).glob('**/*.json')
#
#            for path in files:
#                constant = self.parse_single_constant(path)
#                
#                constant_name = constant['name']
#                constant_abstract_type = constant['abstract_type']
#                constant_obj = Constant(constant_abstract_type, constant_name)
#
#                database.constants[constant_name] = constant_obj
#       
#    def parse_single_constant(self) -> Dict[str, Any]:
#        with open(path) as constantfile:
#            return json.loads(constantfile) 

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

    def parse_functions(self, path: Path, database: Database) -> None:
        # load defaults
        defaults_filename = path / 'defaults.json'
        with defaults_filename.open() as default_file:
            defaults = json.load(default_file)

        # load single file
        function_filename = path / 'functions.json'
        if function_filename.exists():
            raise NotImplementedError

        # load directory function definitions
        functions_directory = path / 'functions/'
        if functions_directory.is_dir():
            files = functions_directory.glob('**/*.json')

            for path in files:
                func = self.parse_single_function(path.absolute())
                self.default_function(func, defaults)
                
                func_obj = Function(database, func)

                database.add_function(func_obj)

    def parse_single_function(self, path: Path) -> Dict[str, Any]:
        with open(path) as funcfile:
            return json.load(funcfile)

    def parse_types(self, path: Path, database: Database) -> None:
        # load single file definitions
        types_filename = path / 'types.json'
        if types_filename.is_file():
            with types_filename.open() as types_file:
                type_array = json.load(types_file)

                for mpi_type in type_array:
                    database.add_type(Type(database, mpi_type))
        
        # TODO load directory definitions
#        types_directory = path + 'types/'
#        if os.path.isdir(types_directory):
#            files = pathlib.Path(types_directory).glob('**/*.json')
#
#            for path in files:
#                mpi_type = self.parse_single_type(path)
#                
#                type_name = mpi_type['name']
#                type_abstract_type = mpi_type['abstract_type']
#                type_ctype = mpi_type['ctype']
#
#                type_source = mpi_type['source']
#                for source in type_source:
#                    if source == "range":
#                        type_lower_range = mpi_type['range'][0]
#                        type_upper_range = mpi_type['range'][1]
#
#                type_obj = Type(type_abstract_type,
#                                type_source,
#                                type_ctype,
#                                [type_lower_range, type_upper_range], 
#                                type_name)
#
#                database.add_type(type_obj)

    def parse_single_type(self, path: Path)-> Dict[str, Any]:
        with path.open() as typefile:
            return json.load(typefile)
