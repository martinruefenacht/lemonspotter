"""
This module defines the initiation point to finalization point generator.
"""

import logging
from typing import Iterable, MutableSet, MutableMapping, Optional

from core.test import Test, TestType, TestOutcome
from core.variable import Variable
from core.database import Database
from core.function import Function, FunctionSample
from core.testgenerator import TestGenerator
from core.instantiator import Instantiator
from core.statement import FunctionStatement, ConditionStatement, DeclarationAssignmentStatement


class StartEndGenerator(TestGenerator):
    """
    Source code generator for initiator and finalizer functions.
    """

    def __init__(self, database: Database) -> None:
        super().__init__(database)

        self.elements_generated = 0

    def generate(self, instantiator: Instantiator) -> Iterable[Test]:
        """
        Generate all possible C programs for all initiators and finalizers.
        """

        # determine all start functions
        starts = filter(lambda f: (not (f.needs_all or f.needs_any) and
                        (f.leads_any or f.leads_all)) and f.present,
                        self._database.functions)

        # determine all end points
        ends = filter(lambda f: (not (f.leads_all or f.leads_any) and
                      (f.needs_any or f.needs_all)) and f.present,
                      self._database.functions)

        # for all combinations
        tests: MutableSet[Test] = set()

        for start in starts:
            logging.info('using start %s', str(start))

            for end in ends:
                logging.info('using start %s', str(start))

                # generate individual test
                logging.debug('generating tests for %s-%s with %s', start, end, instantiator)
                for test in self._gen_tests(start, end, instantiator):
                    tests.add(test)

        return tests

    def _gen_tests(self, start: Function, end: Function, sampler: Instantiator) -> Iterable[Test]:
        """
        Using the functions selected and the given instantiator generate a test
        for each argument set extracted from instantiator.
        """

        tests: MutableSet[Test] = set()
        test_base_name = '_'.join([func.name for func in [start, end]])

        # generate function samples
        samples: MutableMapping[Function, MutableSet[FunctionSample]] = {}

        for function in [start, end]:
            if function not in samples:
                samples[function] = set()

            for sample in sampler.generate_samples(function):
                samples[function].add(sample)

        # generate testcases
        for sidx, start_sample in enumerate(samples[start]):
            for eidx, end_sample in enumerate(samples[end]):
                # generate unique id
                test_specifier = eidx + len(samples[start]) * sidx

                logging.info('generating test of %s and %s', str(start_sample), str(end_sample))
                test = self._gen_test(test_base_name + '_' + str(test_specifier),
                                      start_sample, end_sample)

                tests.add(test)

        return tests

    def _gen_test(self, test_name: str, start: FunctionSample, end: FunctionSample) -> Test:
        """
        Generate C source code for a given path between initiator and finalizer.
        """

        source = self._gen_main()

        # generate start
        for variable in start.arguments:
            if variable.name not in source.variables:
                source.add_at_start(DeclarationAssignmentStatement(variable))
    
        source.add_at_start(start.generate_statement(source))
        source.add_at_start(FunctionStatement.generate_print(start.return_variable))
        source.add_at_start(ConditionStatement.generate_check(start.return_variable))

        # generate end
        for variable in end.arguments:
            if variable.name not in source.variables:
                source.add_at_start(DeclarationAssignmentStatement(variable))

        source.add_at_start(end.generate_statement(source))
        source.add_at_start(FunctionStatement.generate_print(end.return_variable))
        source.add_at_start(ConditionStatement.generate_check(end.return_variable))

        # create test
        test = Test(test_name, TestType.BUILD_AND_RUN, source)
        logging.debug('test %s source:\n' + repr(test.source).replace('%', '%%'), test.name)

        def run_success():
            
            if start.evaluator() and end.evaluator():
                test.run_outcome = TestOutcome.SUCCESS
                logging.info('test %s succeded.', test.name)
            
            else:
                test.run_outcome = TestOutcome.FAILED

                logging.info('test %s failed.', test.name)

        # register return_start return_end
        test.register_capture(start.return_variable)
        test.register_capture(end.return_variable)

        test.run_success_function = run_success

        return test
