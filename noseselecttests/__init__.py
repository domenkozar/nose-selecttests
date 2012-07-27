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
                          "parameter")

    def configure(self, options, config):
        """Configure the plugin and system, based on selected options.
        """
        self.selected_tests = []
        self.unselected_tests = []

        for test_name in options.selected_tests:
            if not test_name:
                continue
            if test_name[0] == "!":
                self.unselected_tests.append(test_name[1:])
            else:
                self.selected_tests.append(test_name)

        if self.selected_tests or self.unselected_tests:
            self.enabled = True

    def _is_selected(self, name):
        """Based on configuration and name of the test determine
        if it should be selected or not.
        """
        selected = False
        for pattern in self.selected_tests:
            if not pattern.endswith('*'):
                pattern = pattern + '*'
            if not pattern.startswith('*'):
                pattern = '*' + pattern
            if name is None or fnmatch(name.lower(), pattern.lower()):
                # name will be None when we have SyntaxError,
                # report that in any case
                selected = True

        if selected == True:
            for pattern in self.unselected_tests:
                if not pattern.endswith('*'):
                    pattern = pattern + '*'
                if not pattern.startswith('*'):
                    pattern = '*' + pattern
                if fnmatch(name.lower(), pattern.lower()):
                    selected = False
        return selected

    def prepareTestCase(self, test):
        """Nose plugin method to filter out tests that haven't been selected.
        """
        name = test.address()[-1]
        if not self._is_selected(name):
            return lambda x: None
