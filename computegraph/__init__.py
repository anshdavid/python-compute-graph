# -*- coding: utf-8 -*-
# _____________________________________________________________________________
# @File    :   _init__.py
# @Time    :   2023/04/11 13:58:31
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
import logging.handlers
import sys
import time


logging.root.setLevel(logging.NOTSET)
LOG_FORMAT = "%(levelname)-8s %(module)-10s:%(lineno)-3s - %(message)s"

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
CONSOLE_HANDLER.setStream(sys.stdout)
logging.root.addHandler(CONSOLE_HANDLER)
