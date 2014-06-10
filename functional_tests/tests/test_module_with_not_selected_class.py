from unittest import TestCase


def test_bare_function_that_is_selected():
    print('should be called')


def test_bare_function_that_is_not_selected():
    assert 0 == 'should not be called'


class TestClassWithSetupNotSelected_that_is_not_selected(TestCase):

    @classmethod
    def setUpClass(self):
        assert 0 == 'setUpClass should not be called'

    @classmethod
    def tearDownClass(self):
        assert 0 == 'tearDownClass should not be called'

    def setUp(self):
        assert 0 == 'setUp should not be called'
        
    def tearDown(self):
        assert 0 == 'tearDown should not be called'

    def test_method_that_is_not_selected(self):
        assert 0 == 'should not be called'

