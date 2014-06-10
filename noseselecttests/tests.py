import os
import unittest

from nose.pyversion import unbound_method
from nose.plugins import PluginTester

from noseselecttests import NoseSelectPlugin


class DummyOptParser(object):
    def __init__(self):
        self.opts = []

    def add_option(self, *args, **kw):
        self.opts.append((args, kw))


def fobj(par):
    pass


def configure_complex():
    pass


class DummyTest(object):
    __module__ = 'noseselecttests.tests'

    def __init__(self):
        pass

    def test_foo(self):
        return False


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

    def test_is_selected_function(self):
        plugin = NoseSelectPlugin()

        plugin.add_criterion('fobj')
        self.assertTrue(plugin._is_selected(fobj))

    def test_is_selected_case_insensitive(self):
        plugin = NoseSelectPlugin()
        plugin.add_criterion('fObJ')
        self.assertTrue(plugin._is_selected(fobj))

    def test_is_selected_wildcard(self):
        plugin = NoseSelectPlugin()
        plugin.add_criterion('configure*complex')
        self.assertTrue(plugin._is_selected(configure_complex))

    def test_is_selected_false(self):
        plugin = NoseSelectPlugin()
        plugin.add_criterion('foobar')
        self.assertFalse(plugin._is_selected(fobj))

    def test_is_selected_selects_module(self):
        plugin = NoseSelectPlugin()
        plugin.add_criterion('noseselecttests.tests')
        self.assertTrue(plugin._is_selected(DummyTest))

    def test_is_selected_selects_class(self):
        plugin = NoseSelectPlugin()
        plugin.add_criterion('DummyTest')
        self.assertTrue(plugin._is_selected(DummyTest))

    def test_is_selected_selects_method_unbound(self):
        plugin = NoseSelectPlugin()
        plugin.add_criterion('DummyTest.test_foo')
        self.assertTrue(plugin._is_selected(unbound_method(DummyTest, DummyTest.test_foo)))

    def test_is_selected_selects_method_bound(self):
        plugin = NoseSelectPlugin()
        plugin.add_criterion('DummyTest.test_foo')
        self.assertTrue(plugin._is_selected(DummyTest().test_foo))


# functional tests using the nose PluginTester

base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'functional_tests')


class NoseSelectPluginTesterPositiveTest(PluginTester, unittest.TestCase):
    activate = ''
    plugins = [NoseSelectPlugin()]
    suitepath = base_dir
    args = ['-v', '--exe', '--select-tests=is_selected']

    def test_selection_is_correct(self):
        assert all(x in self.output
                   for x in ['tests.test_module.TestClassWithSetupAndSelectedMethod_but_Class_that_is_not_selected',
                             'tests.test_module.test_bare_function_that_is_selected',
                             'tests.test_module_with_not_selected_class.test_bare_function_that_is_selected',])


class NoseSelectPluginTesterIvertedTest(PluginTester, unittest.TestCase):
    activate = ''
    plugins = [NoseSelectPlugin()]
    suitepath = base_dir
    args = ['-v', '--exe', '--select-tests=is_not_selected']

    def test_selection_is_correctly_inverted(self):
        assert all(x in self.output
                   for x in ['FAIL: tests.test_module_with_not_selected_class.test_bare_function_that_is_not_selected',
                             "ERROR: test suite for <class 'tests.test_module_with_not_selected_class.TestClassWithSetupNotSelected_that_is_not_selected'>",
                             'test_method_that_is_not_selected (tests.test_module.TestClassWithSetupAndSelectedMethod_but_Class_that_is_not_selected) ... ok',
                             'test_method_that_is_selected (tests.test_module.TestClassWithSetupAndSelectedMethod_but_Class_that_is_not_selected) ... ok',
        ])
