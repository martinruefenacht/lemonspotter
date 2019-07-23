"""
"""

from typing import Dict, Any
import logging

from core.database import Database
from core.type import Type

class Constant:
    """
    """
    
    def __init__(self, database: Database, json: Dict[str, Any]):
        """
        """

        self._database: Database = database
        self._json: Dict[str, Any] = json
        self._value: str = None

        self._properties = {}

    @property
    def name(self) -> str:
        return self._json['name']
    
    @property
    def type(self) -> Type:
        return self._database.types_by_abstract_type[self._json['abstract_type']]

    @property
    def properties(self) -> Dict[str, Any]:
        return self._properties

    @property
    def defined(self) -> bool:
        """
        """

        spec_defined = self._json.get('defined', None) is not None
        logging.debug('constant %s is defined %s', self.name, str(spec_defined))

        return spec_defined

    def validate(self) -> bool:
        """

        """
        
        value = self._properties.get('value', None)
        if value is not None:
            logging.debug('constant has value, operand %s', self._json['defined']['operand'])

            if self._json['defined']['operand'] == 'equal':
                if self._json['defined']['value'] == value:
                    logging.info('validating constant %s', self.name)
                    self._properties['valid'] = True

                else:
                    logging.critical('constant %s failed to validate', self.name)
                    self._properties['valid'] = False

            else:
                logging.error('unknown operand')
                raise RuntimeError("unknown operand")

        return self._properties.get('valid', False)
