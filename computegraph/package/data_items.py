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

from computegraph.framework.base import CGProtocolDataItem


class Boolean(CGProtocolDataItem):
    def __init__(self, value: bool):
        self._value = value

    def SetValue(self, value: bool):
        self._value = value

    def GetValue(self) -> bool:
        return self._value

    def GetType(self) -> Type:
        return bool


class String(CGProtocolDataItem):
    def __init__(self, value: str):
        self._value = value

    def SetValue(self, value: str):
        self._value = value

    def GetValue(self) -> str:
        return self._value

    def GetType(self) -> Type:
        return str


class Integer(CGProtocolDataItem):
    def __init__(self, value: int):
        self._value = value

    def SetValue(self, value: int):
        self._value = value

    def GetValue(self) -> int:
        return self._value

    def GetType(self) -> Type:
        return int
