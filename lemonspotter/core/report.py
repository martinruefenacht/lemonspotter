import datetime

class TestReport():
    def init(self):
        self._now = datetime.datetime.now()
        self._report_id = "lsout_" + self._now.strftime("%Y-%m-%d_%H:%M")

    def parse_results(self):
    """
    Interpret results of test
    """
        raise NotImplementedError

    def log_test_result(self, test ,msg):
    """
    Write output of test to console
    """
        raise NotImplementedError

    def write_presence_report(self) -> str:
        """
        Writes presence_report to report file
        """
        report_file_name = self.report_id + '.log'
        with open('../../reports/' + report_file_name, 'a+') as report_file:       
            presence_report = ''

            for constant in self._database.constants:
                presence_report += constant.name + '\t\t ' + str(constant.properties) + '\n'

            presence_report += '\n' + '#' * 80 + '\n\n'

            for function in self._database.functions:
                presence_report += function.name + '\t\t ' + str(function.properties) + '\n'

            report_file.write(presence_report)

    def write(self):
    """
    Write output of test to file for permanent storage
    """
        raise NotImplementedError
