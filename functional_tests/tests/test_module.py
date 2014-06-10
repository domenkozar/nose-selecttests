from unittest import TestCase


def test_bare_function_that_is_selected():
    print('test_bare_function should be called')


class TestClassWithSetupAndSelectedMethod_but_Class_that_is_not_selected(TestCase):

    @classmethod
    def setUpClass(self):
        print('setUpClass should be called')

    @classmethod
    def tearDownClass(self):
        print('tearDownClass should be called')

    def setUp(self):
        print('setUp should be called')
        
    def tearDown(self):
        print('tearDown should be called')

    def test_method_that_is_not_selected(self):
        print('should not be called')

    def test_method_that_is_selected(self):
        print('test_method_that_is_selected should be called')
