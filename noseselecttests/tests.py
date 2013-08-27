import os
import unittest

from nose.plugins import PluginTester
from noseselecttests import NoseSelectPlugin
from nose.plugins.base import Plugin


class DummyOptParser(object):
    def __init__(self):
        self.opts = []

    def add_option(self, *args, **kw):
        self.opts.append((args, kw))


class CObj(object):
    pass


def fobj(par):
    pass


def build_tst_object(type, module, cls, func):
    '''Return a test object with its names set properly'''
    o = CObj
    o.__name__ = cls
    o.__module__ = module
    f = fobj
    f.__name__ = func
    f.__module__ = module
    setattr(o,func,f)
    if type == 'meth':
        return f
    if type == 'func':
        return f
    if type == 'class':
        return o


class DummyTest(object):

    def __init__(self, name):
        #self.name = name
        self.__name__ = name
    def address(self):
        return [self.name]


class NoseSelectPluginTest(unittest.TestCase):

    def _get_options(self, selected_tests):
        class Options:
            pass

        options = Options()
        options.selection_criteria = selected_tests
        return options

    def _get_config(self):
        import nose.config
        return nose.config.Config()

    def test_configure_none(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options([]), self._get_config())

        self.assertEqual(plugin.selection_criteria, [])
        self.assertFalse(plugin.enabled)

    def test_configure_empty_string(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options(['']), self._get_config())

        self.assertEqual(plugin.selection_criteria, [])
        self.assertFalse(plugin.enabled)

    def test_configure_simple(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options(['Foobar']), self._get_config())

        self.assertEqual(plugin.selection_criteria, ['*foobar*'])
        self.assertTrue(plugin.enabled)

    def test_configure_or(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options(['foobar', 'FOO']), self._get_config())

        self.assertEqual(plugin.selection_criteria, ['*foobar*', '*foo*'])
        self.assertTrue(plugin.enabled)

    def test_is_selected_simple(self):
        to = build_tst_object('func', 
                          module='noseselecttests.tests', 
                          cls='NoseSelectPluginTest', 
                          func= 'test_configure_complex')
        plugin = NoseSelectPlugin()

        plugin.add_criterion('configure')
        self.assertTrue(plugin._is_selected(to))

    def test_is_selected_case_insensitive(self):
        to = build_tst_object('func', 
                          module='noseselecttests.tests', 
                          cls='NoseSelectPluginTest', 
                          func= 'test_configure_complex')
        plugin = NoseSelectPlugin()
        plugin.add_criterion('ConfigurE_CompLex')
        self.assertTrue(plugin._is_selected(to))

    def test_is_selected_wildcard(self):
        to = build_tst_object('func', 
                          module='noseselecttests.tests', 
                          cls='NoseSelectPluginTest', 
                          func= 'test_configure_complex')
        plugin = NoseSelectPlugin()
        plugin.add_criterion('configure*complex')
        self.assertTrue(plugin._is_selected(to))

    def test_is_selected_negative(self):
        to = build_tst_object('func', 
                          module='noseselecttests.tests', 
                          cls='NoseSelectPluginTest', 
                          func= 'test_configure_complex')
        plugin = NoseSelectPlugin()
        plugin.add_criterion('foobar')
        self.assertFalse(plugin._is_selected(to))

    def test_is_selected_selects_module(self):
        to = build_tst_object('func', 
                          module='noseselecttests.tests', 
                          cls='NoseSelectPluginTest', 
                          func= 'test_configure_complex')
        plugin = NoseSelectPlugin()
        plugin.add_criterion('noseselecttests.tests')
        self.assertTrue(plugin._is_selected(to))

    def test_is_selected_selects_class(self):
        to = build_tst_object('class', 
                          module='noseselecttests.tests', 
                          cls='NoseSelectPluginTest', 
                          func= 'test_configure_complex')
        plugin = NoseSelectPlugin()
        plugin.add_criterion('NoseSelectPluginTest')
        self.assertTrue(plugin._is_selected(to))

    def test_is_selected_selects_method_unbound(self):
        to = build_tst_object('class', 
                          module='noseselecttests.tests', 
                          cls='NoseSelectPluginTest', 
                          func= 'test_configure_complex')
        plugin = NoseSelectPlugin()
        plugin.add_criterion('NoseSelectPluginTest.test_configure_complex')
        self.assertTrue(plugin._is_selected(to.test_configure_complex))

    def test_is_selected_selects_method_bound(self):
        to = build_tst_object('class', 
                          module='noseselecttests.tests', 
                          cls='NoseSelectPluginTest', 
                          func= 'test_configure_complex')
        to = to().test_configure_complex
        plugin = NoseSelectPlugin()
        plugin.add_criterion('NoseSelectPluginTest.test_configure_complex')
        self.assertTrue(plugin._is_selected(to))


base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'functional_tests')

#functional tests using the nose PluginTester
class NoseSelectPluginTesterPositiveTest(PluginTester, unittest.TestCase):
    activate = ''
    plugins = [NoseSelectPlugin()]
    suitepath = base_dir
    args = ['-v', '--exe','--select-tests=is_selected' ]

    def test_selection_is_correct(self):
        assert all(x in self.output 
                   for x in ['tests.test_module.TestClassWithSetupAndSelectedMethod_but_Class_that_is_not_selected',
                             'tests.test_module.test_bare_function_that_is_selected',
                             'tests.test_module_with_not_selected_class.test_bare_function_that_is_selected',])


class NoseSelectPluginTesterIvertedTest(PluginTester, unittest.TestCase):
    activate = ''
    plugins = [NoseSelectPlugin()]
    suitepath = base_dir
    args = ['-v', '--exe','--select-tests=is_not_selected' ]

    def test_selection_is_correctly_inverted(self):
        print self.output
        assert all(x in self.output 
                   for x in ['FAIL: tests.test_module_with_not_selected_class.test_bare_function_that_is_not_selected',
                             "ERROR: test suite for <class 'tests.test_module_with_not_selected_class.TestClassWithSetupNotSelected_that_is_not_selected'>",
                             'test_method_that_is_not_selected (tests.test_module.TestClassWithSetupAndSelectedMethod_but_Class_that_is_not_selected) ... ok',
                             'test_method_that_is_selected (tests.test_module.TestClassWithSetupAndSelectedMethod_but_Class_that_is_not_selected) ... ok',
        ])
