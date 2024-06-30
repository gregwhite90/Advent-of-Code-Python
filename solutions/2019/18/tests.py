import unittest
import importlib

from .solution import Solution
from solutions.shared.utils import parse_input

class Tests(unittest.TestCase):
    def setUp(self):
        self.soln = Solution()
    
    def test_example_1(self):
        parse_input(self.soln, [], filename='solutions/2019/18/input/test_examples/example_1.txt')
        self.assertEqual(8, self.soln.solve())

    def test_example_2(self):
        parse_input(self.soln, [], filename='solutions/2019/18/input/test_examples/example_2.txt')
        self.assertEqual(86, self.soln.solve())

    def test_example_3(self):
        parse_input(self.soln, [], filename='solutions/2019/18/input/test_examples/example_3.txt')
        self.assertEqual(132, self.soln.solve())

    def test_example_4(self):
        parse_input(self.soln, [], filename='solutions/2019/18/input/test_examples/example_4.txt')
        self.assertEqual(136, self.soln.solve())
        
    def test_example_5(self):
        parse_input(self.soln, [], filename='solutions/2019/18/input/test_examples/example_5.txt')
        self.assertEqual(81, self.soln.solve())
    
if __name__ == '__main__':
    unittest.main()