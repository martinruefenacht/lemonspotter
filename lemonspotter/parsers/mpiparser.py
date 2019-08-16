from pathlib import Path
import json
from typing import Mapping, Any, Sequence
import logging

from core.database import Database
from core.function import Function
from core.type import Type
from core.constant import Constant


class MPIParser:
    def __call__(self, database_path: Path) -> Database:
        return self.parse(database_path)

    def parse(self, database_path: Path) -> None:
        self.parse_types(database_path)
        self.parse_constants(database_path)
        self.parse_functions(database_path)

    def parse_constants(self, path: Path) -> None:
        # parse single file
        constants_filename = path / 'constants.json'

        if constants_filename.exists():
            with constants_filename.open() as constants_file:
                constants_array = json.load(constants_file)

                for constant in constants_array:
                    Database().add_constant(Constant(constant))

        # parse subdirectory of constants
        # constants_directory = path / 'constants/'
        # if constants_directory.is_dir():
        #     files = constants_directory.glob('**/*.json')

        #     for path in files:
        #         #constant = self.parse_single_constant(path.absolute())

        #         database.add_constant(Constant(database, constant))
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

    def parse_functions(self, path: Path) -> None:
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

                func_obj = Function(func)

                Database().add_function(func_obj)

    def parse_single_function(self, path: Path) -> Mapping[str, Any]:
        with open(path) as funcfile:
            return json.load(funcfile)

    def parse_types(self, path: Path) -> None:
        # load single file definitions
        types_filename = path / 'types.json'
        if types_filename.is_file():
            with types_filename.open() as types_file:
                self.parse_type_definitions(json.load(types_file))

        else:
            logging.info('Types file does not exist.')

        # load directory definitions
        types_directory = path / 'types/'

        if types_directory.is_dir():
            for path in types_directory.glob('**/*.json'):
                with path.open() as type_file:
                    type_data = json.load(type_file)

                    if isinstance(type_data, list):
                        self.parse_type_definitions(type_data)

                    else:
                        Database().add_type(Type(type_data))

        else:
            logging.info('Types directory does not exist: %s', str(types_directory))

    def parse_type_definitions(self, type_definitions: Sequence[Any]) -> None:
        """
        """

        for type_definition in type_definitions:
            Database().add_type(Type(type_definition))
