"""
This module defines the initiation point to finalization point generator.
"""

import logging
from typing import Iterable, MutableSet, MutableMapping

from core.test import Test, TestType, TestOutcome
from core.database import Database
from core.function import Function
from core.sample import FunctionSample
from core.testgenerator import TestGenerator
from core.sampler import Sampler


class StartEndGenerator(TestGenerator):
    """
    Source code generator for initiator and finalizer functions.
    """

    def __init__(self, database: Database) -> None:
        super().__init__(database)

        self.elements_generated = 0

    def generate(self, sampler: Sampler) -> Iterable[Test]:
        """
        Generate all possible C programs for all initiators and finalizers.
        """

        # determine all start functions
        starts = list(filter(lambda f: (not (f.needs_all or f.needs_any) and
                             (f.leads_any or f.leads_all)) and f.present,
                             self._database.functions))

        # determine all end points
        ends = list(filter(lambda f: (not (f.leads_all or f.leads_any) and
                           (f.needs_any or f.needs_all)) and f.present,
                           self._database.functions))

        # for all combinations
        tests: MutableSet[Test] = set()

        for start in starts:
            for end in ends:
                # generate individual test
                logging.debug('generating tests for %s-%s with %s', start, end, sampler)
                for test in self._gen_tests(start, end, sampler):
                    tests.add(test)

        return tests

    def _gen_tests(self, start: Function, end: Function, sampler: Sampler) -> Iterable[Test]:
        """
        Using the functions selected and the given sampler generate a test
        for each argument set extracted from sampler.
        """

        tests: MutableSet[Test] = set()
        test_base_name = f'{start.name}_{end.name}'

        # generate function samples
        samples: MutableMapping[Function, MutableSet[FunctionSample]] = {}

        for function in (start, end):
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
                test = self._gen_test(f'{test_base_name}_{test_specifier}',
                                      start_sample, end_sample)

                tests.add(test)

        return tests

    def _gen_test(self, test_name: str, start: FunctionSample, end: FunctionSample) -> Test:
        """
        Generate C source code for a given path between initiator and finalizer.
        """

        source = self._gen_main()

        logging.debug(start)
        start.generate_source(source)

        logging.debug(end)
        end.generate_source(source)

        # create test
        test = Test(test_name, TestType.BUILD_AND_RUN, source)

        def run_success():
            if start.evaluator() and end.evaluator():
                test.run_outcome = TestOutcome.SUCCESS

            else:
                test.run_outcome = TestOutcome.FAILED
                logging.warning('%s test failed.', test.name)

        test.run_success_function = run_success

        return test
