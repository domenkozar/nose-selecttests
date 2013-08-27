
import logging
from fnmatch import fnmatch
from types import ClassType, ModuleType

from nose.plugins.base import Plugin
from nose.selector import Selector

log = logging.getLogger(__name__)


class MockPlugins(object):
    '''Mock "plugins" that does nothing to avoid infinite recursion calls 
       from Selector'''

    def wantClass(self, cls):
        return None
    def wantDirectory(self, dirname):
        return None
    def wantFile(self, file):
        return None
    def wantFunction(self, function):
        return None
    def wantMethod(self, method):
        return None
    def wantModule(self, module):
        return None


class NoseSelectPlugin(Plugin):
    """Selects test to run based on tests names matching a pattern."""

    def options(self, parser, env):
        """Register command line options"""
        parser.add_option("-t", "--select-tests",
                          dest="selection_criteria", action="append",
                          default=list(),
                          metavar="SELECT",
                          help="Only run tests with a name matching a case-insensitive glob pattern (See fnmatch)")

    def _as_pattern(self, criterion):
        # transforms selection criteria in glob patterns
        return '*%s*' % criterion.lower().strip('*')

    def add_criterion(self, criterion):
        #used mostly for testing
        if not hasattr(self, 'selection_criteria'):
            self.selection_criteria = []
        self.selection_criteria.append(self._as_pattern(criterion))

    def configure(self, options, config):
        self.selection_criteria = [self._as_pattern(criterion) 
                                   for criterion in options.selection_criteria
                                   if criterion and criterion.strip()]

        if self.selection_criteria:
            self.enabled = True

        # use a base selector to ensure we are additive to the basic selection
        self.base_selector = Selector(config)
        self.base_selector.configure(config)
        # we use a mock for plugins to avoid our plugin to be called 
        # in a loop from the Selector (and avoid an infinite loop)
        self.base_selector.plugins = MockPlugins()

    def _is_selected(self, test_obj):
        """Return True if a test object should be selected based on criteria pattern."""
        if not test_obj:
            return
        if isinstance(test_obj, basestring):
            name = test_obj
        else:
            name = objname(test_obj)
        #log.debug('object name: %r' % name)
        if name:
            name = name.lower()
            matched = lambda pat: fnmatch(name, pat)
            selected = any(matched(pat) for pat in self.selection_criteria)
            #log.debug('selected:%r name: %r' % (selected, name,))
            return selected
        else:
            return False

    def wantMethod(self, method):
        return self.base_selector.wantMethod(method) and self._is_selected(method)

    def wantFunction(self, function):
        return self.base_selector.wantFunction(function) and self._is_selected(function)


def objname(obj):
    '''Return the context qualified name of a function, method or class obj'''
    if hasattr(obj, 'name'):
        return obj.name
    # name proper
    if hasattr(obj, '__name__'):
        names = [obj.__name__]
    else:
        #this is a class?
        names = [obj.__class__.__name__]
    # parent class if method
    if hasattr(obj, 'im_class'):
        # this is a method
        names.insert(0, obj.im_class.__name__)
    #module, but ignore __main__ module
    if hasattr(obj, '__module__') and not obj.__module__.startswith('_'):
        names.insert(0, obj.__module__)
    name = '.'.join(names)
    return name
