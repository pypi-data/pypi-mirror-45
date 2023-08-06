import time, unittest
from django.conf import settings
from django.test.runner import DiscoverRunner
from unittest.runner import TextTestResult


class TimeLoggingTestResult(TextTestResult):

    def __init__(self, *args, **kwargs):
        super(TimeLoggingTestResult, self).__init__(*args, **kwargs)
        self.test_timings = []

    def startTest(self, test):
        self._test_started_at = time.time()
        super(TimeLoggingTestResult, self).startTest(test)

    def addSuccess(self, test):
        elapsed = time.time() - self._test_started_at
        name = self.getDescription(test)
        self.test_timings.append((name, elapsed))
        super(TimeLoggingTestResult, self).addSuccess(test)


# Django agnostic
class TimedUnitTestRunner(unittest.TextTestRunner):

    def __init__(self, *args, **kwargs):
        self.slow_test_threshold = float(getattr(settings, 'TIMED_TEST_THRESHOLD_SECS', 0.0))
        kwargs['resultclass'] = TimeLoggingTestResult
        return super(TimedUnitTestRunner, self).__init__(*args, **kwargs)

    def run(self, test):
        result = super(TimedUnitTestRunner, self).run(test)
        self.stream.writeln("\nTest Times (>{:.03}s):".format(self.slow_test_threshold))
        has_slow = False

        # sort slowest to fastest
        result.test_timings.sort(key=lambda x: x[1], reverse=True)

        for name, elapsed in result.test_timings:
            if elapsed > self.slow_test_threshold:
                self.stream.writeln("  [{:.03}s] {}".format(round(elapsed, 3), name))
                has_slow = True

        if not has_slow:
            self.stream.writeln('  None')

        self.stream.writeln(' ')

        return result


# Django specific
class TimedTestRunner(DiscoverRunner):

    test_runner = TimedUnitTestRunner

    def get_resultclass(self):
        return TimeLoggingTestResult
