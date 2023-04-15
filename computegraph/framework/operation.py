# -*- coding: utf-8 -*-
# _____________________________________________________________________________
# @File    :   operation.py
# @Time    :   2023/04/11 21:22:01
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
from typing import Any, Dict, List

from computegraph.framework.base import BaseOperation


class CGOperation(BaseOperation):
    class Modifiers:
        class OptionalData(str):
            def __repr__(self) -> str:
                return f"OptionalData{self}"

    def Compute(self, input_dict: Dict, output_list: List[str] | None = None) -> Dict:
        to_exec = self.function

        inputs = [input_dict[d] for d in self.inputs if not isinstance(d, CGOperation.Modifiers.OptionalData)]

        optionals = {
            n: input_dict[n]
            for n in self.inputs
            if isinstance(n, CGOperation.Modifiers.OptionalData) and n in input_dict
        }

        kwargs = {k: v for d in (self.attr_dict, optionals) for k, v in d.items()}

        result: List = []
        try:
            result = to_exec(*inputs, **kwargs) if kwargs else to_exec(*inputs)
        except ValueError as e:
            logging.error(e)
            return {}
        except Exception as e:
            logging.critical(e)
            return {}

        if len(self.outputs) == 1:
            result = [result]

        ret_dict = zip(self.outputs, result)
        if output_list:
            ret_dict = filter(lambda kv: kv[0] in set(output_list), ret_dict)

        return dict(ret_dict)
