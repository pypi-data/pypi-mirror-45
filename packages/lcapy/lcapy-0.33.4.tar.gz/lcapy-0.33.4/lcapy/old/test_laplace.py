from lcapy import *
import unittest


class LcapyTester(unittest.TestCase):

    """Unit tests for lcapy

    """

    def test_laplace(self):

        self.assertEqual(Heaviside(t).laplace(), 1 / s, "Heaviside(t)")
        self.assertEqual(DiracDelta(t).laplace(), 1, "DiracDelta(t)")

    def test_inverse_laplace(self):

        self.assertEqual((1 / s).inverse_laplace(causal=True), Heaviside(t),
                         "1 / s")
        self.assertEqual((s * 0 + 1).inverse_laplace(causal=True), DiracDelta(t),
                         "1")
        self.assertEqual((s * 0 + 10).inverse_laplace(causal=True), 10
                         * DiracDelta(t), "0")                
