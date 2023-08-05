from lcapy import *
import unittest


class LcapyTester(unittest.TestCase):

    def assertEqual2(self, ans1, ans2, comment):

        try:
            self.assertEqual(ans1, ans2, comment)
        except AssertionError as e:
            pprint(ans1)
            pprint(ans2)
            raise AssertionError(e)

    def test_pretty(self):

        a = expr(3)
        self.assertEqual2(pretty(a), '3', "pretty(a)")
        self.assertEqual2(a.pretty(), '3', "a.pretty()")
        self.assertEqual2(latex(a), '3', "a.latex()")
        self.assertEqual2(a.latex(), '3', "a.latex()")
        self.assertEqual2(a.latex_math(), '$3$', "a.latex_math()")        
        
        
        
