# COMPUTE-GRAPH

Task shceduling and execution. 

> To serve as a backend framework for `No-Code` front end application('visual node editor').


## Compute network

Computation graph creation for lazy execution

    op_network = CGNetwork("test network")

    op_sub = CGOperation("op_sub", ["a", "b"], ["a_minus_b"], sub)
    op_div = CGOperation("op_div", ["a_minus_b", "c"], ["a_minus_b_div_c"], truediv)
    op_pow = CGOperation("op_pow", ["a_minus_b_div_c", "p"], ["a_minus_b_div_c_pow_p"], pow)
    op_mul = CGOperation("op_mul", ["x", "y"], ["p"], mul)

    op_network.Compile(optimize=False)

    op_network({"a": 0.3, "b": 4, "c": 11, "x": 7, "y": -2})

## Eager Execuion

To serve as a backend from a simple `Node Editor` or `Visual Programming Tool`

    input_node_a = string_node("input_node_a", "developer")
    input_node_b = string_node("input_node_b", "")
    concate_node = concat_node("concat_node")

    
    input_node_a.GetSocketByName("input_node_a_socket_out").Connect(
        concate_node.GetSocketByName("concat_node_socket_in_a")
    )
    input_node_b.GetSocketByName("input_node_b_socket_out").Connect(
        concate_node.GetSocketByName("concat_node_socket_in_b")
    )

    input_node_b.GetInterfaceByName("input_node_b_string_data").UpdateValue("working")

    print(concate_node.GetSocketByName("concat_node_socket_out_c").GetValue() == "developer_working)
    
**Test Samples [here](./test) # It works!**
