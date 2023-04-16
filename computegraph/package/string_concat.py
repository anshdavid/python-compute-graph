# -*- coding: utf-8 -*-
# _____________________________________________________________________________
# @File    :   data_items.py
# @Time    :   2023/04/12 11:28:47
# _____________________________________________________________________________

"""A one line summary of the module or program, terminated by a period.

Leave one blank line. The rest of this docstring should contain an overall 
description of the module or program.  Optionally, it may also contain a 
brief description of exported classes and functions and/or usage examples.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension
"""


from __future__ import annotations
from typing import Type

from computegraph.framework.base import SocketTypeEnum
from computegraph.framework.node import CGNode
from computegraph.package.data_items import String


def string_node(node_name: str, init_value: str) -> CGNode:
    node = CGNode(node_name)
    node_string_data = node.AddData(f"{node_name}_string_data", String(init_value))
    node_socket_out = node.AddSocket(f"{node_name}_socket_out", SocketTypeEnum.OUTPUT)
    node_socket_out.SetDataInterface(node_string_data)
    return node


def concat_node(node_name: str, separator: str = "_") -> CGNode:
    def concate_operation(a, b):
        return "_".join([a, b])

    concate_node = CGNode(node_name)

    concate_node_data_a = concate_node.AddData(f"{node_name}_data_a", String(""))
    concate_node_data_b = concate_node.AddData(f"{node_name}_data_b", String(""))
    concate_node_data_c = concate_node.AddData(f"{node_name}_data_c", String(""))

    concate_node_socket_in_a = concate_node.AddSocket(f"{node_name}_socket_in_a", SocketTypeEnum.INPUT)
    concate_node_socket_in_b = concate_node.AddSocket(f"{node_name}_socket_in_b", SocketTypeEnum.INPUT)
    concate_node_socket_out_c = concate_node.AddSocket(f"{node_name}_socket_out_c", SocketTypeEnum.OUTPUT)

    concate_node_socket_in_a.SetDataInterface(concate_node_data_a)
    concate_node_socket_in_b.SetDataInterface(concate_node_data_b)
    concate_node_socket_out_c.SetDataInterface(concate_node_data_c)

    concate_node.AddOperation(
        "concate_operation",
        [concate_node_data_a.name, concate_node_data_b.name],
        [concate_node_data_c.name],
        concate_operation,
    )

    return concate_node
