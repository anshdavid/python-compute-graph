# -*- coding: utf-8 -*-
# _____________________________________________________________________________
# @File    :   abstract.py
# @Time    :   2023/04/10 21:06:16
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
from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import Any, Dict, List, Protocol


class AbstractItem(ABC):
    @property
    @abstractmethod
    def name(self):
        ...

    @name.setter
    @abstractmethod
    def name(self, value):
        ...

    @property
    @abstractmethod
    def uid(self):
        ...

    @uid.setter
    @abstractmethod
    def uid(self, value):
        ...


class CGProtocolDataItem(Protocol):
    def SetValue(self, *args, **kwargs):
        ...

    def GetValue(self):
        ...

    def GetType(self):
        ...


class AbstractDatainterface(ABC):
    @property
    @abstractmethod
    def parent_node(self):
        ...

    @property
    @abstractmethod
    def data_item(self) -> CGProtocolDataItem:
        ...

    @abstractmethod
    def GetValue(self):
        ...

    @abstractmethod
    def SetValue(self, *args, **kwargs):
        ...

    @abstractmethod
    def UpdateValue(self, *args, **kwargs):
        ...


class AbstractSocket(ABC):
    @property
    @abstractmethod
    def parent_node(self):
        ...

    @property
    @abstractmethod
    def socket_type(self):
        ...

    @property
    @abstractmethod
    def connections(self):
        ...

    @property
    @abstractmethod
    def data_interface(self):
        ...

    @abstractmethod
    def Connect(self, *args, **kwargs):
        ...

    @abstractmethod
    def Disconnect(self, *args, **kwargs):
        ...

    @abstractmethod
    def SetDataInterface(self, *args, **kwargs):
        ...

    @abstractmethod
    def GetValue(self):
        ...

    @abstractmethod
    def UpdateValue(self, *args, **kwargs):
        ...

    @abstractmethod
    def Propogate(self):
        ...


class AbstractNode(ABC):
    @property
    @abstractmethod
    def sockets(self):
        ...

    @property
    @abstractmethod
    def data_interfaces(self):
        ...

    @property
    @abstractmethod
    def operations(self):
        ...

    @abstractmethod
    def GetValues(self):
        ...

    @abstractmethod
    def GetSocketByName(self):
        ...

    @abstractmethod
    def GetInterfaceByName(self):
        ...

    @abstractmethod
    def SetValues(self, *args, **kwargs):
        ...

    @abstractmethod
    def UpdateValues(self, *args, **kwargs):
        ...

    @abstractmethod
    def AddSocket(self, *args, **kwargs):
        ...

    @abstractmethod
    def AddData(self, *args, **kwargs):
        ...

    @abstractmethod
    def AddOperation(self, *args, **kwargs):
        ...

    @abstractmethod
    def Evaluate(self, *args, **kwargs):
        ...

    @abstractmethod
    def Compute(self):
        ...

    @abstractmethod
    def Execute(self, *args, **kwargs):
        ...

    @abstractmethod
    def Propogate(self):
        ...


class AbstractOperation(ABC):
    @property
    @abstractmethod
    def inputs(self):
        ...

    @property
    @abstractmethod
    def outputs(self):
        ...

    @property
    @abstractmethod
    def attr_dict(self):
        ...

    @property
    @abstractmethod
    def function(self):
        ...

    @abstractmethod
    def Compute(self, *args, **kwargs):
        ...


class AbstractNetwork(ABC):
    @property
    @abstractmethod
    def graph(self):
        ...

    @property
    @abstractmethod
    def perf_register(self):
        ...

    @property
    @abstractmethod
    def flag_compiled(self):
        ...

    @property
    @abstractmethod
    def ordered_steps(self):
        ...

    @property
    @abstractmethod
    def cached_requirements(self):
        ...

    @abstractmethod
    def AddOperation(self, *args, **kwargs):
        ...

    @abstractmethod
    def AddOperations(self, *args, **kwargs):
        ...

    @abstractmethod
    def Compile(self, *args, **kwargs):
        ...

    @abstractmethod
    def EvaluateComputationRequirements(self, *args, **kwargs):
        ...

    @abstractmethod
    def __call__(self, *args, **kwargs):
        ...
