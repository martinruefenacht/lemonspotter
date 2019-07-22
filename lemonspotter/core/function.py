"""    Defines an function object that can be included in Lemonspotter tests."""

from typing import Dict, List

from core.variable import Variable
from core.statement import Statement
from core.database import Database
from core.statement import BlockStatement, FunctionStatement

class MainDefinitionStatement(BlockStatement):
    def __init__(self, database: Database) -> None:
        super().__init__()

        argc = Variable(database.type_by_abstract_type['INT'],
                        'argument_count')
        argv = Variable(database.type_by_abstract_type['CHAR'],
                        'argument_list',
                        pointer_level=2)

        self._variables[argc.name] = argc
        self._variables[argv.name] = argv

        self._statement = 'int main(int argument_count, char **argument_list)'

    def express(self) -> str:
        return self._statement + '\n' + super().express()

class Function:
    """
    Defines an function object that can be included in Lemonspotter tests.
    """

    def __init__(self, name, return_type, parameters, needs_any, needs_all, leads_any, leads_all):
        """
        Initializes function element.

        Parameters:
        name         (string)    : Name of the function
        return_type  (string)    : Coorespondes to what this function is supposed to return
        parameters   (string[])  : List of items that this function takes as a parameter
        needs_any    (string[])  : TODO
        needs_all    (string[])  : TODO
        leads_any    (string[])  : TODO
        leads_all    (string[])  : TODO
        """

        self._name = name
        self._parameters = parameters
        self._return_type = return_type

        self._needs_any = needs_any
        self._needs_all = needs_all

        self._leads_any = leads_any
        self._leads_all = leads_all

        # TODO think about how to handle this
        # present vs not present is a boolean
        # validated is true for certain arguments, but not others
        # attempted is really quite useless
        self._attempted = False
        self._validated = False

        self.properties = {}

    def __repr__(self) -> str:
        """
        Defines informal string behavior for function type
        """
        return self._name

    def __str__(self) -> str:
        """
        Defines formal string behavior for function type
        """
        return self._name

    def generate_function_statement(self, arguments: List[Variable], return_name: str, database: Database) -> FunctionStatement:
        """
        Generates a compilable expression of the function with the given arguments.
        """

        statement = ''

        #statement += self.return_type.kind + ' ' + return_name
        statement += database.type_by_abstract_type[self.return_type].language_type + ' ' + return_name

        return_variable = Variable(database.type_by_abstract_type[self.return_type], return_name)

        statement += ' = '
        statement += self.name + '('

        # add arguments
        for idx, (argument, parameter) in enumerate(zip(arguments, self._parameters)):
            mod = ''

            pointer_diff = argument.pointer_level - parameter['pointer']
            if pointer_diff > 0:
                # dereference *
                raise NotImplementedError

            elif pointer_diff < 0:
                # addressof &
                mod += '&'

            statement += (mod + argument.name)

            if (idx + 1) != len(arguments):
                statement += ', '

        statement += ');'

        return FunctionStatement(statement, {return_name: return_variable})

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = parameters

    @property
    def return_type(self):
        return self._return_type
    
    @return_type.setter
    def return_type(self, return_type):
        self._return_type = return_type

    @property
    def needs_any(self):
        return self._needs_any
    
    @needs_any.setter
    def needs_any(self, needs_any):
        self._needs_any = needs_any

    @property
    def needs_all(self):
        return self._needs_all
    
    @needs_all.setter
    def needs_all(self, needs_all):
        self._needs_all = needs_all

    @property
    def leads_any(self):
        return self._leads_any
    
    @leads_any.setter
    def leads_any(self, leads_any):
        self._leads_any = leads_any

    @property
    def leads_all(self):
        return self._leads_all
    
    @leads_all.setter
    def leads_all(self, leads_all):
        self._leads_all = leads_all

    @property
    def validated(self):
        return self._validated

    @validated.setter
    def validated(self, validated):
        self._validated = validated

    @property
    def attempted(self):
        return self._attempted

    @attempted.setter
    def attempted(self, attempted):
        self._attempted = attempted

    @property
    def presence_tested(self):
        return self._presence_tested
    
    @presence_tested.setter
    def presence_tested(self, presence_tested):
        self._presence_tested = presence_tested

    @property
    def present(self):
        return self._present

    @present.setter
    def present(self, present):
        self._present = present

    def has_failed(self):
        """
        Deterministic test to determine if function has failed tests
        """
        return self._attempted and not self._validated

    def validate(self):
        """
        Sets the validation state of the function to true
        """
        self._validated = True

    def invalidate(self):
        """
        Sets the validation state of the function to false
        """
        self._validated = True

    def attempt(self):
        """
        Sets the attempt state of the function
        """
        self._attempted = True
