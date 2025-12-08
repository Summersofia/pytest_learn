import pytest
class Test_class(object):
    def test_case_hello(self):
        print('这里是测试类,Here successful test class.')
        assert True
    def test_case_hello2(self):
        print('这里是测试类,Here failed test class.')
        assert False