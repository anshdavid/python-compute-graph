# -*- coding: utf-8 -*-
# _____________________________________________________________________________
# @File    :   _base.py
# @Time    :   2023/04/10 22:39:21
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
from abc import abstractmethod
from collections import OrderedDict as ordered_dict

from typing import Any, Callable, Dict, List, Set, OrderedDict
from enum import IntEnum, auto

import networkx


from computegraph.framework.abstract import (
    AbstractDatainterface,
    AbstractItem,
    AbstractNetwork,
    AbstractNode,
    AbstractOperation,
    AbstractSocket,
    CGProtocolDataItem,
)
from computegraph.utils import UUID


class ItemType(IntEnum):
    NODE = auto()
    SOCKET = auto()
    DATA_INTERFACE = auto()
    OPERATION = auto()


class SocketTypeEnum(IntEnum):
    INPUT = auto()
    OUTPUT = auto()


class BaseItem(AbstractItem):
    def __init__(self, name: str, uid: str | None = None):
        self._name = name
        self._uid = uid or UUID()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, uid: str):
        self._uid = uid


class BaseDataInterface(BaseItem, AbstractDatainterface):
    def __init__(
        self,
        parent_node: BaseNode,
        name: str,
        data_item: CGProtocolDataItem,
        uid: str | None = None,
    ):
        super().__init__(name, uid)
        self._parent_node = parent_node
        self._data_item = data_item

    @property
    def parent_node(self) -> BaseNode:
        return self._parent_node

    @property
    def data_item(self) -> CGProtocolDataItem:
        return self._data_item

    def GetValue(self) -> Any:
        raise NotImplementedError("")

    def SetValue(self, value: Any):
        raise NotImplementedError("")

    def UpdateValue(self, value: Any):
        raise NotImplementedError("")


class BaseSocket(BaseItem, AbstractSocket):
    def __init__(
        self,
        parent_node: BaseNode,
        name: str,
        socket_type: SocketTypeEnum,
        uid: str | None = None,
    ):
        super().__init__(name, uid)

        self._parent_node = parent_node
        self._socket_type = socket_type
        self._data_interface: BaseDataInterface | None = None

        self._connections: Set[BaseSocket] = set()

    @property
    def parent_node(self) -> BaseNode:
        return self._parent_node

    @property
    def socket_type(self) -> SocketTypeEnum:
        return self._socket_type

    @property
    def connections(self) -> List[BaseSocket]:
        return list(self._connections)

    @property
    def data_interface(self) -> BaseDataInterface | None:
        return self._data_interface

    def Connect(self, *args, **kwargs):
        raise NotImplementedError("")

    def Disconnect(self, *args, **kwargs):
        raise NotImplementedError("")

    def SetDataInterface(self, interface: BaseDataInterface) -> None:
        raise NotImplementedError("")

    def GetValue(self) -> Any | None:
        raise NotImplementedError("")

    def UpdateValue(self, value: Any):
        raise NotImplementedError("")

    def Propogate(self):
        raise NotImplementedError("")


class BaseNode(BaseItem, AbstractNode):
    def __init__(self, name: str, uid: str | None = None):
        super().__init__(name, uid)
        self._sockets: List = []
        self._data_interfaces: List = []
        self._operations: List = []

    @property
    def sockets(self) -> List[BaseSocket]:
        return self._sockets

    @property
    def data_interfaces(self) -> List[BaseDataInterface]:
        return self._data_interfaces

    @property
    def operations(self) -> List[BaseOperation]:
        return self._operations

    def GetValues(self) -> Dict:
        raise NotImplementedError("")

    def SetValues(self, value_dict: Dict):
        raise NotImplementedError("")

    def UpdateValues(self, value_dict: Dict):
        raise NotImplementedError("")

    def AddSocket(
        self,
        socket_name: str,
        socket_type: SocketTypeEnum,
        max_connections: int,
        uid: str | None = None,
    ) -> BaseSocket | None:
        raise NotImplementedError("")

    def AddData(
        self, name: str, data_item: CGProtocolDataItem, uid: str | None = None
    ) -> BaseDataInterface | None:
        raise NotImplementedError("")

    def AddOperation(
        self,
        name: str,
        inputs: List[str],
        outputs: List[str],
        function: Callable,
        params: Dict,
        uid: str | None,
    ) -> BaseOperation | None:
        raise NotImplementedError("")

    def Evaluate(self, *args, **kwargs):
        raise NotImplementedError("")

    def Compute(self):
        raise NotImplementedError("")

    def Execute(self, *args, **kwargs):
        raise NotImplementedError("")

    def Propogate(self):
        raise NotImplementedError("")


class BaseOperation(BaseItem, AbstractOperation):
    def __init__(
        self,
        name: str,
        inputs: List[str],
        outputs: List[str],
        function: Callable,
        attr_dict: Dict = {},
        uid: str | None = None,
    ):
        # sourcery skip: default-mutable-arg
        super().__init__(name, uid)
        self._inputs: List[str] = inputs
        self._outputs: List[str] = outputs
        self._function: Callable = function
        self._attr_dict: Dict = attr_dict

    @property
    def inputs(self) -> List[str]:
        return self._inputs

    @property
    def outputs(self) -> List[str]:
        return self._outputs

    @property
    def attr_dict(self) -> Dict:
        return self._attr_dict

    @property
    def function(self) -> Callable:
        return self._function

    def __repr__(self) -> str:
        return f"Operation(name:`{self.name}` in:`{self.inputs} out:`{self.outputs}`)"

    def Compute(self, *args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("")


class BaseNetwork(BaseItem, AbstractNetwork):
    def __init__(self, name: str, uid: str | None = None):
        super().__init__(name, uid)

        self._graph = networkx.DiGraph()
        self._perf_register: OrderedDict[str, float | int] = ordered_dict()
        self._flag_compiled = False
        self._ordered_steps: List[Any] = []
        self._cached_requirements: Dict = {}

    @property
    def graph(self):
        return self._graph

    @property
    def perf_register(self):
        return self._perf_register

    @property
    def flag_compiled(self):
        return self._flag_compiled

    @property
    def ordered_steps(self):
        return self._ordered_steps

    @property
    def cached_requirements(self):
        return self._cached_requirements

    def AddOperation(self, *args, **kwargs):
        raise NotImplementedError("")

    def AddOperations(self, *args, **kwargs):
        raise NotImplementedError("")

    def Compile(self, *args, **kwargs):
        raise NotImplementedError("")

    def EvaluateComputationRequirements(self, *args, **kwargs):
        raise NotImplementedError("")

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("")
