import unittest

from noseselecttests import NoseSelectPlugin


class DummyOptParser(object):
    def __init__(self):
        self.opts = []

    def add_option(self, *args, **kw):
        self.opts.append((args, kw))


class DummyTest(object):

    def __init__(self, name, exc_class=None):
        self.name = name
        if exc_class:
            class Test():
                pass
            self.test = Test()
            self.test.exc_val = exc_class()
        else:
            self.test = None

    def address(self):
        return [self.name]


class NoseSelectPluginTest(unittest.TestCase):

    def _get_options(self, selected_tests):
        class Options:
            pass

        options = Options()
        options.selected_tests = selected_tests
        return options

    def test_options(self):
        plugin = NoseSelectPlugin()
        parser = DummyOptParser()
        plugin.add_options(parser)

        self.assertEqual(parser.opts, [
            (('-t', '--select-tests'),
             {'action': 'append',
              'default': [],
              'dest': 'selected_tests',
              'help': 'Run only tests that match case-insensitive to this parameter',
              'metavar': 'SELECT'})
        ])

    def test_configure_none(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options([]), None)

        self.assertEqual(plugin.selected_tests, [])
        self.assertFalse(plugin.enabled)

    def test_configure_empty_string(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options(['']), None)

        self.assertEqual(plugin.selected_tests, [])
        self.assertFalse(plugin.enabled)

    def test_configure_simple(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options(['foobar']), None)

        self.assertEqual(plugin.selected_tests, ['foobar'])
        self.assertTrue(plugin.enabled)

    def test_configure_or(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options(['foobar', 'foo']), None)

        self.assertEqual(plugin.selected_tests, ['foobar', 'foo'])
        self.assertTrue(plugin.enabled)

    def test_is_selected_simple(self):
        name = "noseselecttests.tests.NoseSelectPluginTest.test_configure_complex"
        plugin = NoseSelectPlugin()

        plugin.selected_tests = ['configure']
        self.assertTrue(plugin._is_selected(DummyTest(name)))

    def test_is_selected_SyntaxError(self):
        # means we have SyntaxError in this file
        name = None
        plugin = NoseSelectPlugin()

        plugin.selected_tests = ['configure']
        self.assertTrue(plugin._is_selected(DummyTest(name, exc_class=SyntaxError)))

    def test_is_selected_case_insensitive(self):
        name = "noseselecttests.tests.NoseSelectPluginTest.test_configure_complex"
        plugin = NoseSelectPlugin()
        plugin.selected_tests = ['noseselectplugintest']
        self.assertTrue(plugin._is_selected(DummyTest(name)))

    def test_is_selected_wildcard(self):
        name = "noseselecttests.tests.NoseSelectPluginTest.test_configure_complex"
        plugin = NoseSelectPlugin()
        plugin.selected_tests = ['configure*complex']
        self.assertTrue(plugin._is_selected(DummyTest(name)))

    def test_is_selected_negative(self):
        name = "noseselecttests.tests.NoseSelectPluginTest.test_configure_complex"
        plugin = NoseSelectPlugin()
        plugin.selected_tests = ['foobar']
        self.assertFalse(plugin._is_selected(DummyTest(name)))

    def test_prepareTestCase_select(self):
        plugin = NoseSelectPlugin()
        plugin._is_selected = lambda x: True
        self.assertEqual(plugin.prepareTestCase(DummyTest('foobar')), None)

    def test_prepareTestCase_exclude(self):
        plugin = NoseSelectPlugin()
        plugin._is_selected = lambda x: False
        self.assertEqual(plugin.prepareTestCase(DummyTest('foobar'))('test'), None)
