"""
The StandardParser parses the apis.json emitted by the MPI Standard
pythonization effort.
"""


import json
import sys
import logging
from typing import Mapping, MutableMapping


from pathlib import Path


from lemonspotter.core.database import Database
from lemonspotter.core.function import Function


class StandardParser:
    """
    This class is a parser for the MPI Standard.
    """

    def __call__(self, database_path: Path) -> None:
        if database_path.suffix != '.json':
            raise RuntimeError(f'The given database path is not a json file: '
                               f'{database_path}')

        with database_path.open() as encoded:
            apis = json.load(encoded)

            for name, definition in apis.items():
                if 'lemonspotter' in definition and definition['lemonspotter']:
                    self._parse_API(definition)

    def _parse_API(self, definition: Mapping) -> None:
        """
        Parse the API definition from the MPI Standard.
        """

        translation = {}

        translation['name'] = definition['name']
        translation['return'] = definition['return_kind']
        translation['needs_any'] = definition['attributes']['needs_any']
        translation['needs_all'] = definition['attributes']['needs_all']
        translation['leads_any'] = definition['attributes']['leads_any']
        translation['leads_all'] = definition['attributes']['leads_all']
        translation['parameters'] = []

        for parameter in definition['parameters']:
            param = {}

            param['name'] = parameter['name']
            param['abstract_type'] = parameter['kind']
            param['direction'] = param['param_direction']
            param['length'] = param['length']

            # TODO pointer
            # TODO const

            translation['parameters'].append(param)

        # TODO filter, valid combinations of parameters

        Database().add_function(Function(translation))


if __name__ == '__main__':
    parser = StandardParser()
    parser(Path(sys.argv[1]))

    print(Database()._functions)

    for function in Database()._functions:
        print(function._json)
