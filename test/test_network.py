import unittest

from computegraph.framework.network import CGNetwork
from computegraph.framework.operation import CGOperation
from operator import sub, truediv, pow, mul


class TestClass(unittest.TestCase):
    def test_network_operation(self):
        op_network = CGNetwork("test network")

        op_sub = CGOperation("op_sub", ["a", "b"], ["a_minus_b"], sub)
        op_div = CGOperation("op_div", ["a_minus_b", "c"], ["a_minus_b_div_c"], truediv)
        op_pow = CGOperation("op_pow", ["a_minus_b_div_c", "p"], ["a_minus_b_div_c_pow_p"], pow)
        op_mul = CGOperation("op_mul", ["x", "y"], ["p"], mul)

        op_network.AddOperations([op_sub, op_div, op_pow, op_mul])

        op_network.Compile(optimize=False)

        result = op_network({"a": 0.3, "b": 4, "c": 11, "x": 7, "y": -2})

        self.assertEqual(result["a_minus_b"], -3.7)
        self.assertEqual(round(result["a_minus_b_div_c"], 3), -0.336)
        self.assertEqual(round(result["a_minus_b_div_c_pow_p"], 3), 4213795.503)
