import unittest
from computegraph.framework.base import SocketTypeEnum

from computegraph.package.data_items import Boolean, String
from computegraph.framework.node import CGNode
from operator import ior, iand, not_

from computegraph.package.string_concat import concat_node, string_node


class TestClass(unittest.TestCase):
    def test_simple_operation(self):
        test = CGNode("test_simple_operation")
        test.AddData("bool_in_1", Boolean(False))
        test.AddData("bool_in_2", Boolean(False))
        test.AddData("bool_out_1", Boolean(False))

        test.AddOperation("op_ior", ["bool_in_1", "bool_in_2"], ["bool_out_1"], ior)

        test.SetValues({"bool_in_1": True, "bool_in_2": False})
        test.Compute()
        self.assertEqual(test.GetValues()["bool_out_1"], True)

        test.UpdateValues({"bool_in_1": False})
        self.assertEqual(test.GetValues()["bool_out_1"], False)

    def test_nested_operation_iterim_result(self):
        test = CGNode("test_nested_operation_iterim_result")
        bool_in_1 = test.AddData("bool_in_1", Boolean(False))
        bool_in_2 = test.AddData("bool_in_2", Boolean(False))
        bool_interim_3 = test.AddData("bool_interim_3", Boolean(False))
        bool_out_1 = test.AddData("bool_out_1", Boolean(False))

        test.AddOperation("op_ior", ["bool_in_1", "bool_in_2"], ["bool_interim_3"], iand)

        test.AddOperation("op_not", ["bool_interim_3"], ["bool_out_1"], not_)

        test.Compute()
        self.assertEqual(bool_interim_3.GetValue(), False)
        self.assertEqual(bool_out_1.GetValue(), True)

        bool_in_1.UpdateValue(True)
        self.assertEqual(bool_interim_3.GetValue(), False)
        self.assertEqual(bool_out_1.GetValue(), True)

        bool_in_2.UpdateValue(True)
        self.assertEqual(bool_interim_3.GetValue(), True)
        self.assertEqual(bool_out_1.GetValue(), False)

    def test_concat_node(self):
        input_node_a = string_node("input_node_a", "developer")
        input_node_b = string_node("input_node_b", "")
        concate_node = concat_node("concat_node")

        input_node_a.GetSocketByName("input_node_a_socket_out").Connect(  # type:ignore
            concate_node.GetSocketByName("concat_node_socket_in_a")
        )
        input_node_b.GetSocketByName("input_node_b_socket_out").Connect(  # type:ignore
            concate_node.GetSocketByName("concat_node_socket_in_b")
        )

        input_node_b.GetInterfaceByName("input_node_b_string_data").UpdateValue("working")  # type:ignore

        self.assertEqual(
            concate_node.GetSocketByName("concat_node_socket_out_c").GetValue(),  # type:ignore
            "developer_working",
        )
