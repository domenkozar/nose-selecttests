import unittest

from noseselecttests import NoseSelectPlugin


class MockOptParser(object):
    def __init__(self):
        self.opts = []

    def add_option(self, *args, **kw):
        self.opts.append((args, kw))


class NoseSelectPluginTest(unittest.TestCase):

    def _get_options(self, selected_tests):
        class Options:
            pass

        options = Options()
        options.selected_tests = selected_tests
        return options

    def test_options(self):
        plugin = NoseSelectPlugin()
        parser = MockOptParser()
        plugin.add_options(parser)

        self.assertEqual(parser.opts, [
            (('-t', '--select-tests'),
             {'action': 'append',
              'default': [],
              'dest': 'selected_tests',
              'help': 'Run only tests that match case-insensitive to thisparameter',
              'metavar': 'SELECT'}
        )])

    def test_configure_none(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options([]), None)

        self.assertEqual(plugin.selected_tests, [])
        self.assertEqual(plugin.unselected_tests, [])
        self.assertFalse(plugin.enabled)

    def test_configure_empty_string(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options(['']), None)

        self.assertEqual(plugin.selected_tests, [])
        self.assertEqual(plugin.unselected_tests, [])
        self.assertFalse(plugin.enabled)

    def test_configure_simple(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options(['foobar']), None)

        self.assertEqual(plugin.selected_tests, ['foobar'])
        self.assertEqual(plugin.unselected_tests, [])
        self.assertTrue(plugin.enabled)

    def test_configure_complex(self):
        plugin = NoseSelectPlugin()
        plugin.configure(self._get_options(['foobar', '!test', 'foo', '!boo']), None)

        self.assertEqual(plugin.selected_tests, ['foobar', 'foo'])
        self.assertEqual(plugin.unselected_tests, ['test', 'boo'])
        self.assertTrue(plugin.enabled)

    def test_is_selected_simple(self):
        name = "noseselecttests.tests.NoseSelectPluginTest.test_configure_complex"
        plugin = NoseSelectPlugin()

        plugin.selected_tests = ['configure']
        plugin.unselected_tests = []
        self.assertTrue(plugin._is_selected(name))

    def test_is_selected_None(self):
        # means we have SyntaxError in this file
        name = None
        plugin = NoseSelectPlugin()

        plugin.selected_tests = ['configure']
        plugin.unselected_tests = []
        self.assertTrue(plugin._is_selected(name))

    def test_is_selected_case_insensitive(self):
        name = "noseselecttests.tests.NoseSelectPluginTest.test_configure_complex"
        plugin = NoseSelectPlugin()
        plugin.selected_tests = ['noseselectplugintest']
        plugin.unselected_tests = []
        self.assertTrue(plugin._is_selected(name))

    def test_is_selected_wildcard(self):
        name = "noseselecttests.tests.NoseSelectPluginTest.test_configure_complex"
        plugin = NoseSelectPlugin()
        plugin.selected_tests = ['configure*complex']
        plugin.unselected_tests = []
        self.assertTrue(plugin._is_selected(name))

    def test_is_selected_negative(self):
        name = "noseselecttests.tests.NoseSelectPluginTest.test_configure_complex"
        plugin = NoseSelectPlugin()
        plugin.selected_tests = ['foobar']
        plugin.unselected_tests = []
        self.assertFalse(plugin._is_selected(name))

    def test_is_selected_unselected_override(self):
        name = "noseselecttests.tests.NoseSelectPluginTest.test_configure_complex"
        plugin = NoseSelectPlugin()
        plugin.selected_tests = ['configure']
        plugin.unselected_tests = ['complex']
        self.assertFalse(plugin._is_selected(name))

    def test_is_selected_unselected(self):
        name = "noseselecttests.tests.NoseSelectPluginTest.test_configure_complex"
        plugin = NoseSelectPlugin()
        plugin.selected_tests = []
        plugin.unselected_tests = ['complex']
        self.assertFalse(plugin._is_selected(name))

    def _get_nose_tst(self):
        class Test: pass

        test = Test()
        test.address = lambda: ['foobar']
        return test

    def test_prepareTestCase_select(self):
        plugin = NoseSelectPlugin()
        plugin._is_selected = lambda x: True
        self.assertEqual(plugin.prepareTestCase(self._get_nose_tst()), None)

    def test_prepareTestCase_exclude(self):
        plugin = NoseSelectPlugin()
        plugin._is_selected = lambda x: False
        self.assertEqual(plugin.prepareTestCase(self._get_nose_tst())('test'), None)
