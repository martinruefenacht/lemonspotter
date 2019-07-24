import os, datetime, logging

from core.test import Test

class TestReport():
    def __init__(self, database):
        self._now = datetime.datetime.now()
        self._report_id = "lsout_" + self._now.strftime("%Y-%m-%d_%H:%M")
        self._database = database
    @property
    def report_id(self):
        return self._report_id

    @report_id.setter
    def report_id(self, report_id):
        self._report_id = report_id

    @report_id.deleter
    def report_id(self):
        del self._report_id

    def log_test_result(self, test, msg=None):
        """
        Prints results for single test
        """
        log_msg = ''
        if test.build_outcome and test.run_outcome:
            log_msg += '[PASS] ' + test.name
        else:
            log_msg += '[FAIL] ' + test.name
            
        if msg:
            log_msg += '\n\t' + msg
        
        logging.log(0, log)
        

    def write_presence_report(self):
        """
        Writes presence_report to report file
        """
        if not os.path.exists('../reports/'):
            os.mkdir('../reports')

        report_file_name = self._report_id + '.log'
        with open('../reports/' + report_file_name, 'a+') as report_file:       
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
