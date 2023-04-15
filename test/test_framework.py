import unittest
from computegraph.framework.base import SocketTypeEnum

from computegraph.package.data_items import Boolean, String
from computegraph.framework.node import CGNode
from operator import ior, iand, not_


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
        def concate_operation(a, b):
            return "_".join([a, b])

        node_a = CGNode("node_a")
        node_a_data_a = node_a.AddData("node_a_data_a", String("developer"))
        node_a_socket_out_a = node_a.AddSocket("node_a_socket_out_a", SocketTypeEnum.OUTPUT)
        node_a_socket_out_a.SetDataInterface(node_a_data_a)

        node_b = CGNode("node_b")
        node_b_data_b = node_b.AddData("node_b_data_b", String(""))
        node_b_socket_out_b = node_b.AddSocket("node_b_socket_out_b", SocketTypeEnum.OUTPUT)
        node_b_socket_out_b.SetDataInterface(node_b_data_b)

        concate_node = CGNode("concate_node")

        concate_node_data_a = concate_node.AddData("concate_node_data_a", String(""))
        concate_node_data_b = concate_node.AddData("concate_node_data_b", String(""))
        concate_node_data_c = concate_node.AddData("concate_node_data_c", String(""))

        concate_node_socket_in_a = concate_node.AddSocket("concate_node_socket_in_a", SocketTypeEnum.INPUT)
        concate_node_socket_in_b = concate_node.AddSocket("concate_node_socket_in_b", SocketTypeEnum.INPUT)
        concate_node_socket_out_c = concate_node.AddSocket("concate_node_socket_out_c", SocketTypeEnum.OUTPUT)

        concate_node_socket_in_a.SetDataInterface(concate_node_data_a)
        concate_node_socket_in_b.SetDataInterface(concate_node_data_b)
        concate_node_socket_out_c.SetDataInterface(concate_node_data_c)

        concate_node.AddOperation(
            "concate_operation",
            ["concate_node_data_a", "concate_node_data_b"],
            ["concate_node_data_c"],
            concate_operation,
        )

        node_a_socket_out_a.Connect(concate_node_socket_in_a)
        node_b_socket_out_b.Connect(concate_node_socket_in_b)

        node_b_data_b.UpdateValue("working")
        self.assertEqual(concate_node_socket_out_c.GetValue(), "developer_working")
