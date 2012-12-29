from fnmatch import fnmatch

from nose.plugins.base import Plugin


class NoseSelectPlugin(Plugin):
    """Selects test cases to be run based on their attributes.
    """

    def options(self, parser, env):
        """Register command line options"""
        parser.add_option("-t", "--select-tests",
                          dest="selected_tests", action="append",
                          default=list(),
                          metavar="SELECT",
                          help="Run only tests that match case-insensitive to this"
                          " parameter")

    def configure(self, options, config):
        """Configure the plugin and system, based on selected options.
        """
        self.selected_tests = []

        for test_name in options.selected_tests:
            if not test_name:
                continue
            self.selected_tests.append(test_name)

        if self.selected_tests:
            self.enabled = True

    def _is_selected(self, test):
        """Based on configuration and name of the test determine
        if it should be selected or not.
        """
        name = '.'.join(filter(None, test.address()[-2:]))
        for pattern in self.selected_tests:
            if not pattern.endswith('*'):
                pattern = pattern + '*'
            if not pattern.startswith('*'):
                pattern = '*' + pattern

            if getattr(test.test, 'exc_val', None) and isinstance(test.test.exc_val, SyntaxError):
                # pass SyntaxErrors through to be sure we are not missing something
                return True

            if name and fnmatch(name.lower(), pattern.lower()):
                return True

    def prepareTestCase(self, test):
        """Nose plugin method to filter out tests that haven't been selected.
        """
        if not self._is_selected(test):
            return lambda x: None
