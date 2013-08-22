from fnmatch import fnmatch

from nose.plugins.base import Plugin


class NoseSelectPlugin(Plugin):
    """Selects test to run based on test function or method names using glob patterns (See fnmatch)."""

    def options(self, parser, env):
        """Register command line options"""
        parser.add_option("-t", "--select-tests",
                          dest="selected_tests", action="append",
                          default=list(),
                          metavar="SELECT",
                          help="Only run tests matching this glob pattern (*?[]) (case-insensitive)")

    def configure(self, options, config):
        self.selected_tests = []

        for test_name in options.selected_tests:
            if test_name:
                self.selected_tests.append(test_name)

        if self.selected_tests:
            self.enabled = True

    def _is_selected(self, test_fun):
        """Return True if a test function or method name should be selected based on patterns."""
        if not test_fun:
            return

        name = funame(test_fun)
            
        for pattern in self.selected_tests:
            if not pattern.endswith('*'):
                pattern = pattern + '*'
            if not pattern.startswith('*'):
                pattern = '*' + pattern
            if fnmatch(name.lower(), pattern.lower()):
                return True

        # not None: None means don't care, not False.
        return False 

    def wantFunction(self, function):
        return self._is_selected(function)
    
    def wantMethod(self, method):
        return self._is_selected(method)


def funame(fun):
    '''Return the context qualified name of a function or method'''
    # name proper
    names = [fun.__name__]
    # parent class if method
    if hasattr(fun, 'im_name'):
        # this is a method
        names.insert(0, fun.im_name.__name__)
    #module, but ignore __main__ module
    if not fun.__module__.startswith('_'):
        names.insert(0, fun.__module__)
    
    name = '.'.join(names)
    return name
