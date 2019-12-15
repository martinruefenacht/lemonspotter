"""
This module defines the initiation point to finalization point generator.
"""

import logging
from typing import Iterable, MutableSet, MutableMapping

from lemonspotter.core.test import Test, TestType, TestOutcome
from lemonspotter.core.database import Database
from lemonspotter.core.function import Function
from lemonspotter.core.sample import FunctionSample
from lemonspotter.core.testgenerator import TestGenerator
from lemonspotter.core.sampler import Sampler
from lemonspotter.core.statement import MainDefinitionStatement, ReturnStatement


class IndependentGenerator(TestGenerator):
    """
    Source code generator for initiator and finalizer functions.
    """

    def __init__(self) -> None:
        super().__init__()

        self.elements_generated = 0

    def generate(self, sampler: Sampler) -> Iterable[Test]:
        """
        Generate all possible C programs for all initiators and finalizers.
        """

        # determine all start functions
        independent = list(filter(lambda f: (not (f.needs_all or f.needs_any) and
                             (not (f.leads_any or f.leads_all))) and f.present,
                             Database().get_functions()))

        # for all combinations
        tests: MutableSet[Test] = set()

        for function in independent:
            # generate individual test
            logging.debug('generating tests for %s with %s', function, sampler)
            for test in self._gen_tests(function, sampler):
                tests.add(test)

        return tests

    def _gen_tests(self, function: Function, sampler: Sampler) -> Iterable[Test]:
        """
        Using the functions selected and the given sampler generate a test
        for each argument set extracted from sampler.
        """
        tests: MutableSet[Test] = set()
        test_base_name = f'{function.name}'

        # generate function samples
        samples: MutableMapping[Function, MutableSet[FunctionSample]] = {}

        if function not in samples:
            samples[function] = set()

        for sample in sampler.generate_samples(function):
            samples[function].add(sample)

        # generate testcases
        for idx, function_sample in enumerate(samples[function]):
            # generate unique id
            test_specifier = idx + len(samples[function]) * idx

            logging.info('generating test of %s', str(function_sample))
            test = self._gen_test(f'{test_base_name}_{test_specifier}',
                                  function_sample)

            tests.add(test)

        return tests

    def _gen_test(self, test_name: str, function: FunctionSample) -> Test:
        """
        Generate C source code for a given path between initiator and finalizer.
        """

        source = self._generate_source_frame()

        block_main = MainDefinitionStatement()
        source.add_at_start(block_main)

        block_main.add_at_end(ReturnStatement('0'))

        logging.debug(function)
        function.generate_source(block_main,
                              'start point for independent test')

        # create test
        test = Test(test_name, TestType.BUILD_AND_RUN, source)

        def run_success():
            eval_function = function.evaluator()
            if eval_function:
                test.run_outcome = TestOutcome.SUCCESS

            else:
                test.run_outcome = TestOutcome.FAILED
                logging.warning('%s test failed', test.name)
                logging.debug('with function %s and end %s.', eval_function)

        test.run_success_function = run_success

        return test
