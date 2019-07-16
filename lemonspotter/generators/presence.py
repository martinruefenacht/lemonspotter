"""
This module defines the function presence test generator.
"""

import logging

from core.database import Database
from core.source import Source
from core.testgenerator import TestGenerator

from typing import Set

class PresenceGenearator(TestGenerator):
    def generate(self) -> Set[Source]:
        sources = set()

        # TODO this needs to be rethought
        functions = filter(lambda f: not f._attempted, self._database.functions)

        for func in functions:
            sources.add(self.generate_source(func))

        return sources

    def generate_source(self, function: Function) -> Source:
        """
        This function generates a presence test for the given Function.
        """

        source_name = 'presence_' + function.name
        source, variables = self.generate_main(source_name)

        # instantiate element
        # TODO move this to the Function object, given the Variables

        return source
