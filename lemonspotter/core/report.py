import os, datetime, logging

from core.test import Test, TestStage

class TestReport():
    def __init__(self, database):
        self._now = datetime.datetime.now()
        self._report_id = "lsout_" + self._now.strftime("%Y-%m-%d_%H:%M")
        self._database = database
        
        self._presence_report = None
        self._tests = []
        
    @property
    def report_id(self):
        return self._report_id

    @report_id.setter
    def report_id(self, report_id):
        self._report_id = report_id

    @property
    def presence_report(self):
        return self._presence_report
        
    @presence_report.setter
    def presence_report(self, presence_report):
        self._presence_report = presence_report

    def log_test_result(self, test, msg=None) -> None:
        """
        Prints results for single test
        """
        if test not in self.tests:
            self.tests.append(test)
        
        log_msg = ''
        
        if test.stage == TestStage.BUILD:
            log_msg += '[BUILD]'
            if test.build_outcome:
                log_msg += '[PASS]'
            else:
                log_msg += '[FAIL]'
        elif test.stage == TestStage.RUN:
            log_msg += '[RUN]'
            if test.run_outcome:
                log_msg += '[PASS]'
            else:
                log_msg += '[FAIL]'
        else:
            log_msg += '[STAGE NOT SET]'
            
        log_msg += test.name
        if msg:
            log_msg += '\n\t ' + msg

        logging.log(0, log)
                
                
    def generate_presence_report(self):
        """
        Generates presence_report to report file
        """
        if self._database:
            self.presence_report = ''

            for constant in self._database.constants:
                self.presence_report += constant.name + '\t\t ' + str(constant.properties) + '\n'

            self.presence_report += '\n' + '#' * 80 + '\n\n'

            for function in self._database.functions:
                self.presence_report += function.name + '\t\t ' + str(function.properties) + '\n'
        else:
            self.presence_report = None


    def write_presence_report(self):
        """
        Writes presence_report to report file
        """
        if self.presence_report = None
            self.generate_presence_report()
        
        if not os.path.exists('../reports/'):
            os.mkdir('../reports')

        report_file_name = self._report_id + '.log'
        with open('../reports/' + report_file_name, 'a+') as report_file:
            report_file.write(self.presence_report)
            
    
    def presence_report(self) -> str:
        """
        Prints Presence Report to Console
        """

        if not self.presence_report:
            self.generate_presence_report()

        print(self.presence_report)
        
        


    def write(self):
        """
        Write output of test to file for permanent storage
        """
        raise NotImplementedError
