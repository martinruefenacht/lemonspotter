class TestReport():
    def init(self, test):
        self._test = test
    def parse_results(self):
    """
    Interpret results of test
    """
        raise NotImplementedError

    def log(self, msg):
    """
    Write output of test to console
    """
        raise NotImplementedError

    def write(self):
    """
    Write output of test to file for permanent storage
    """
        raise NotImplementedError
