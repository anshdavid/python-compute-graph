# -*- coding: utf-8 -*-
# _____________________________________________________________________________
# @File    :   node.py
# @Time    :   2023/04/11 19:02:58
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
import logging
from typing import Any, Callable, Dict, List, Optional
from computegraph.framework.abstract import CGProtocolDataItem

from computegraph.framework.base import BaseDataInterface, BaseNode, BaseOperation, BaseSocket, SocketTypeEnum
from computegraph.framework.data import CGDataInterface
from computegraph.framework.operation import CGOperation
from computegraph.framework.socket import CGSocket
from computegraph.utils import UUID


class CGNode(BaseNode):
    def GetSocketByName(self, name: str) -> Optional[BaseSocket]:
        if socket := [socket for socket in self.sockets if socket.name == name]:
            return socket[0]
        return None

    def GetInterfaceByName(self, name: str) -> Optional[BaseDataInterface]:
        if interface := [interface for interface in self.data_interfaces if interface.name == name]:
            return interface[0]
        return None

    def GetValues(self) -> Dict:
        return {interface.name: interface.GetValue() for interface in self.data_interfaces}

    def SetValues(self, value_dict: Dict[str, Any]):
        interface_dict = {interface.name: interface for interface in self.data_interfaces}
        for name, value in value_dict.items():
            if interface := interface_dict.get(name, None):
                interface.SetValue(value)
            else:
                logging.error(f"cannot update interface:`{name}` value, not found in node:`{self.name}`")

    def UpdateValues(self, value_dict: Dict):
        interface_dict = {interface.name: interface for interface in self.data_interfaces}
        for name, value in value_dict.items():
            if interface := interface_dict.get(name, None):
                interface.UpdateValue(value)
            else:
                logging.error(f"cannot update interface:`{name}` value, not found in node:`{self.name}`")

    def AddSocket(self, socket_name: str, socket_type: SocketTypeEnum, uid: str | None = None) -> CGSocket:
        for socket in self.sockets:
            if socket.name == socket_name:
                logging.error(f"socket with name:`{socket_name}` already exsists in node:`{self.name}`")
                exit()
            elif socket.uid == uid:
                logging.error(f"socket with uid:`{uid}` already exsists in node:{self.name}")
                exit()

        socket = CGSocket(self, socket_name, socket_type, uid=uid)
        self.sockets.append(socket)
        return socket

    def AddData(self, name: str, data_item: CGProtocolDataItem, uid: str | None = None) -> CGDataInterface:
        uid = UUID() if uid is None else uid

        if any(name == interf.name for interf in self.data_interfaces):
            logging.error(f"interface with name:`{name}` already exists in node:`{self.name}`")
            exit()

        if any(uid == interf.uid for interf in self.data_interfaces):
            logging.error(f"interface with uid:`{uid}` already exists in node:`{self.name}`")
            exit()

        interface = CGDataInterface(self, name, data_item, uid)
        self.data_interfaces.append(interface)
        return interface

    def AddOperation(
        self,
        name: str,
        inputs: List[str],
        outputs: List[str],
        function: Callable,
        params: Dict = {},
        uid: str | None = None,
    ) -> CGOperation:
        # sourcery skip: default-mutable-arg
        for operation in self.operations:
            if operation.name == name:
                logging.error(f"operation with name:`{name}` already exsists in node:`{self.name}`")
                exit()
        available_data = [interface.name for interface in self.data_interfaces]

        for input_ in inputs:
            if input_ not in available_data:
                logging.error(f"operation input with name:`{input_}` no available in node name:`{self.name}'")
                print("---", available_data)
                exit()

        for output in outputs:
            if output not in available_data:
                logging.error(
                    f"operation output with name:`{output}` no available in node name:`{self.name}'"
                )
                exit()

        operation = CGOperation(name, inputs, outputs, function, params, uid)
        self.operations.append(operation)
        return operation

    def Evaluate(self, interface_name: str):
        for operation in [
            operation_to_compute
            for operation_to_compute in self.operations
            if interface_name in operation_to_compute.inputs
        ]:
            logging.info(f"Evaluate operation called for interface:`{interface_name}`")
            self.Execute(operation)
        self.Propogate()

    def Compute(self):
        for operation in self.operations:
            self.Execute(operation)
        self.Propogate()

    def Execute(self, operation: BaseOperation):
        logging.debug(f"Execute operation:`{operation.name}`")
        result = operation.Compute(self.GetValues())
        self.UpdateValues(result)

    def Propogate(self):
        for socket in [
            socket_to_prop
            for socket_to_prop in self.sockets
            if socket_to_prop.socket_type == SocketTypeEnum.OUTPUT
        ]:
            socket.Propogate()
