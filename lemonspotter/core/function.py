"""    Defines an function object that can be included in Lemonspotter tests."""

from typing import List, Dict, Any, Set, Optional

from core.variable import Variable
from core.database import Database
from core.statement import BlockStatement, FunctionStatement
from core.type import Type
from core.parameter import Parameter

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

    def __init__(self, database: Database, json: Dict[str, Any]) -> None:
        """
        """

        self._database: Database = database
        self._json: Dict[str, Any] = json

        self.properties: Dict[str, Any] = {}

        self._cached_parameters: Optional[List[Parameter]] = None

    def __repr__(self) -> str:
        """
        Defines informal string behavior for function type
        """

        return self._json['name']

    def __str__(self) -> str:
        """
        Defines formal string behavior for function type
        """

        return repr(self)

    def generate_function_statement(self, arguments: List[Variable], return_name: str) -> FunctionStatement:
        """
        Generates a compilable expression of the function with the given arguments.
        """

        statement = ''

        statement += self.return_type.language_type + ' ' + return_name

        return_variable = Variable(self.return_type, return_name)

        statement += ' = '
        statement += self.name + '('

        # add arguments
        for idx, (argument, parameter) in enumerate(zip(arguments, self.parameters)):
            mod = ''

            pointer_diff = argument.pointer_level - parameter.pointer_level
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
    def name(self) -> str:
        return self._json['name']

    @property
    def parameters(self) -> List[Parameter]:
        if self._cached_parameters is None:
            self._cached_parameters = [Parameter(self._database, parameter) for parameter in self._json['parameters']]

        return self._cached_parameters

    @property
    def return_type(self) -> Type:
        return self._database.type_by_abstract_type[self._json['return']]

    @property
    def needs_any(self) -> Set['Function']:
        return set(self._database.functions_by_name[func_name] for func_name in self._json['needs_any'])

    @property
    def needs_all(self) -> Set['Function']:
        return set(self._database.functions_by_name[func_name] for func_name in self._json['needs_all'])

    @property
    def leads_any(self) -> Set['Function']:
        return set(self._database.functions_by_name[func_name] for func_name in self._json['leads_any'])

    @property
    def leads_all(self) -> Set['Function']:
        return set(self._database.functions_by_name[func_name] for func_name in self._json['leads_all'])
