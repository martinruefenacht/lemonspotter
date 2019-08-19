"""
This module contains the definition of the Constant class.
"""

from typing import Dict, Any, Optional
import logging

from core.database import Database
from core.type import Type
from core.variable import Variable


class Constant:
    """
    This class represents a Constant from the specification.
    """

    def __init__(self, json: Dict[str, Any]):
        self._json: Dict[str, Any] = json
        self._value: Optional[str] = None

        self._properties: Dict[str, Any] = {}

    @property
    def name(self) -> str:
        """This property provides the name of the Constant."""

        return self._json['name']

    @property
    def type(self) -> Type:
        """This property provides the Type object from the Constant."""

        return Database().get_type(self._json['abstract_type'])

    @property
    def properties(self) -> Dict[str, Any]:
        """This property provides access to the properties of this Constant."""

        return self._properties

    @property
    def defined(self) -> bool:
        """This property determines whether the constant is defined in the specification."""

        spec_defined = self._json.get('defined', None) is not None
        logging.debug('constant %s is defined %s', self.name, str(spec_defined))

        return spec_defined

    def validate(self) -> bool:
        """This function validates the constant against the specification."""

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

    @property
    def present(self) -> bool:
        """"""

        return self.properties.get('present', False)

    @property
    def valid(self) -> bool:
        """"""

        return self.properties.get('valid', False)

    @property
    def value(self) -> str:
        """"""

        return self.properties['value']

    def generate_variable(self, variable_name: str) -> Variable:
        """
        This generates a Variable object of this constant with a given variable name.
        """

        return Variable(self.type, variable_name, self.name)
