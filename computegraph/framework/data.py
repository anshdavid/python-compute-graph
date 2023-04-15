# -*- coding: utf-8 -*-
# _____________________________________________________________________________
# @File    :   data.py
# @Time    :   2023/04/11 20:44:43
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
from typing import Any

from computegraph.framework.base import BaseDataInterface


class CGDataInterface(BaseDataInterface):
    def GetValue(self) -> Any:
        return self.data_item.GetValue()

    def SetValue(self, value: Any):
        self.data_item.SetValue(value)

    def UpdateValue(self, value: Any):
        current_value = self.data_item.GetValue()
        if current_value != value:
            self.data_item.SetValue(value)
            self.parent_node.Evaluate(self.name)
