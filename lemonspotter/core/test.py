from typing import Union, Dict, List
import os
from core.statement import Statement, BlockStatement
from core.variable import Variable


class Test:
    def __init__(self, name: str, sources: List[Source]=[], expected_result='pass'):
        self._name = name

        self._variables: Dict[str, Variable] = {}

        self._front_statements = []
        self._back_statements = []

        self._build_results = []
        self._exec_results = []

        # Outcome can be pass/fail/xfail/xpass
        self._expected_result = expected_result

        # Actual outcome after tested.
        # Until set default value is ''
        # Once tested can be set to pass/fail/xfail/xpass
        self._result = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        del self._name

    @property
    def variables(self) -> Dict[str, Variable]:
        return self._variables

    def get_variable(self, name: str) -> Variable:
        if name in self._variables:
            return self._variables[name]

        else:
            for statement in self._front_statements:
                if issubclass(type(statement), BlockStatement):
                    if name in statement.variables:
                        return statement.variables[name]

    def add_at_start(self, statement: Statement) -> None:
        """
        Adds a generated string to the front of the source code.
        """

        # TODO currently only able to add to nested block
        if self._front_statements and issubclass(type(self._front_statements[-1]),
                                                 BlockStatement):
            self._front_statements[-1].add_at_start(statement)

        else:
            self._front_statements.append(statement)

            # TODO how to handle this internally?
            # how do statements have access to whole global variables?
            if not issubclass(type(statement), BlockStatement):
                self._variables.update(statement.variables)

    def add_at_end(self, statement: Statement) -> None:
        """
        Adds a generated string to the back of the source code.
        """

        self._back_statements.append(statement)
        self._variables.update(statement.variables)

    def get_source(self) -> str:
        """
        Combines the front and back lines into a single string.
        """

        code = ''

        for statement in self._front_statements:
            code += statement.express() + '\n'

        for statement in self._back_statements:
            code += statement.express() + '\n'

        return code

    @property
    def build_results(self):
        return self._build_results

    @build_results.setter
    def build_results(self, build_results):
        self._build_results = build_results

    @build_results.deleter
    def build_results(self):
        del self._build_results

    @property
    def exec_results(self):
        return self._exec_results

    @exec_results.setter
    def exec_results(self, exec_results):
        self._exec_results = exec_results

    @exec_results.deleter
    def exec_results(self):
        del self._exec_results

    @property
    def expected_result(self):
        return self._expected_result

    @expected_result.setter
    def expected_result(self, expected_result):
        self._expected_result = expected_result

    @expected_result.deleter
    def expected_result(self):
        del self._expected_result

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = result

    @result.deleter
    def result(self):
        del self._result



    def write(self):
        """
        Writes source object to file that can be compiled/run
        by executors.
        """

        # TODO this is hard coding paths

        if not os.path.isdir('../tests'):
            os.makedirs("../tests")

        file_name = self.name + ".c"
        test_file = open("../tests/" + file_name, "w+")

        for line in self.get_source():
            test_file.write(line+"\n")

        test_file.close()

    def build_result_parser(self):
        """
        Fails test if build process produces error
        """
        if self.build_results[1]:
            print("BUILD ERROR: " + self.name + " failed to build.")
            self.result = "failed"

    def exec_result_parser(self):
        """
        Parses output of test execution into results
        """
        if self.expected_result == 'pass':
            if self.exec_results[1]:
                print("STDERR Not Empty")
                print(self.exec_results[1])


class Source:
    def __init__(self, name: str):
        self._name = name
        self._sources = sources

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        del self._name

    @property
    def sources(self):
        return self._sources

    @sources.setter
    def sources(self, sources):
        self._sources = sources

    @sources.deleter
    def sources(self):
        del self._sources

    def write(self):
        """
        Writes source object to file that can be compiled/run
        by executors.
        """
        if not os.path.isdir('../tests'):
            os.makedirs("../tests")

        file_name = self.name + ".c"
        test_file = open("../tests/" + file_name, "w+")

        for source in self.sources:
            test_file.write(source.get_source())

        test_file.close()
