# -*- coding: utf-8 -*-
# _____________________________________________________________________________
# @File    :   socket.py
# @Time    :   2023/04/11 19:53:00
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
from typing import Any

from computegraph.framework.base import BaseDataInterface, BaseSocket


class CGSocket(BaseSocket):
    def Connect(self, socket: BaseSocket):
        if socket not in self.connections:
            self._connections.add(socket)
            self.Propogate()

    def Disconnect(self, socket: BaseSocket):
        self._connections.discard(socket)

    def SetDataInterface(self, interface: BaseDataInterface) -> None:
        self._data_interface = interface

    def GetValue(self) -> Any | None:
        return self.data_interface.GetValue() if self.data_interface else None

    def UpdateValue(self, value: Any, **kwargs):
        if self.data_interface is None:
            logging.debug(f"socket:`{self.name}` has no data interface")
            return

        if self.data_interface.GetValue() == value:
            logging.debug(f"socket:`{self.name}` data interface value has not changed={value}")
            return

        logging.debug(
            f"socket:`{self.name}` updating interface:`{self.data_interface.name}` value={self.data_interface.GetValue()}->{value}"
        )
        self.data_interface.UpdateValue(value)

    def Propogate(self):
        if self.data_interface is None:
            return

        value = self.data_interface.GetValue()

        for socket in self._connections:
            logging.debug(
                f"socket:`{self.name}` updating socket:`{socket.name}` value={socket.GetValue()}->{value}"
            )
            socket.UpdateValue(value)
