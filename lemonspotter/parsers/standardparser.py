"""
The StandardParser parses the apis.json emitted by the MPI Standard
pythonization effort.
"""

import json


from pathlib import Path

from lemonspotter.core.database import Database


class StandardParser:
    """
    This class is a parser for the MPI Standard.
    """

    def __init__(self, database_path: Path) -> None:
        if database_path.suffix != '.json':
            raise RuntimeError(f'The given database path is not a json file: '
                               f'{database_path}')

        with database_path.open() as encoded:
            apis = json.load(encoded)

        for api in apis:
            if 'lemonspotter' in api and api['lemonspotter']:
                # read this api

                print(api)

                # populate database with it
