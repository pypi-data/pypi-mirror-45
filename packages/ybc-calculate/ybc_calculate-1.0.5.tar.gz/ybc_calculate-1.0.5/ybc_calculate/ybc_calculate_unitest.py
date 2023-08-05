import unittest
from ybc_calculate import *


class MyTestCase(unittest.TestCase):
    def test_check(self):
        self.assertRegex(check("test.jpg"), r'test_[0-9]+_result.jpg')
        self.assertEqual(check("test.txt"), -1)

    def test_check_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError,
                                    "^参数类型错误 : 调用check方法时，'image'参数类型错误。$"):
            check(42)


if __name__ == '__main__':
    unittest.main()
