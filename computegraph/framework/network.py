# -*- coding: utf-8 -*-
# _____________________________________________________________________________
# @File    :   network.py
# @Time    :   2023/04/12 17:16:15
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
from enum import IntEnum, auto

import logging
import time
from typing import Any, Callable, Dict, List, Tuple, Union

import networkx as nx

from computegraph.framework.base import BaseNetwork, BaseOperation


class CGNetwork(BaseNetwork):
    class ProcessData(str):
        def __repr__(self):
            return f"ProcessData({self})"

    class DeleteInstruction(str):
        def __repr__(self):
            return f"DeleteInstruction({self})"

    class COMPUTE_METHOD(IntEnum):
        SEQUENTIAL = auto()
        PARALLEL = auto()
        DISTRUBUTED = auto()

    def AddOperation(self, operation: BaseOperation):
        if operation in self._graph.nodes:
            logging.error("Operation can only be added once")
            return

        for n in operation.inputs:
            self._graph.add_edge(CGNetwork.ProcessData(n), operation)

        for p in operation.outputs:
            self._graph.add_edge(operation, CGNetwork.ProcessData(p))

        self._flag_compiled = False

    def AddOperations(self, operations: List[BaseOperation]):
        for operation in operations:
            self.AddOperation(operation)

    def Compile(self, optimize: bool = False) -> List[Union[str, BaseOperation]]:
        # sourcery skip: raise-specific-error
        self.ordered_steps.clear()
        self.cached_requirements.clear()

        try:
            topological_sequence = list(nx.algorithms.dag.topological_sort(self._graph))

            for i, node in enumerate(topological_sequence):
                if isinstance(node, CGNetwork.ProcessData):
                    pass

                elif isinstance(node, BaseOperation):
                    self._ordered_steps.append(node)

                    if optimize:
                        for predecessor in self._graph.predecessors(node):
                            if not any(
                                isinstance(future_node, BaseOperation) and predecessor in future_node.inputs
                                for future_node in topological_sequence[i + 1 :]
                            ):
                                self._ordered_steps.append(CGNetwork.DeleteInstruction(predecessor))

                else:
                    raise Exception(f"unhandles operation type:`{node}`")
        except Exception as e:
            logging.error("Failed to compile network")
            logging.error(e)
            return []

        self._flag_compiled = True
        return list(self.ordered_steps)

    def EvaluateComputationRequirements(
        self, provided_inputs: List[str], requested_outputs: List[str]
    ) -> Tuple[Tuple, Tuple]:
        inputs = tuple(sorted(provided_inputs))
        outputs = tuple(sorted(requested_outputs))

        key = (inputs, outputs)
        if computation_requirements := self.cached_requirements.get(key, None):
            return computation_requirements

        graph = self.graph.copy(as_view=True)
        necessary_nodes = set()
        unnecessary_nodes = set()

        # if inputs are provided, remove preceeding steps in the graph
        for input_name in inputs:
            if graph.has_node(input_name):
                unnecessary_nodes |= nx.dag.ancestors(graph, input_name)
            else:
                logging.warning(f"graph has no OperationData:`{input_name}`")

        # full graph computed
        if not outputs:
            necessary_nodes = set(graph.nodes)

        # for selected outputs, find neccessary ancestors only in the graph
        else:
            for output_name in outputs:
                if graph.has_node(output_name):
                    necessary_nodes |= nx.dag.ancestors(graph, output_name)
                    # unnecessary_nodes |= nx.dag.descendants(graph, output_name)
                else:
                    logging.warning(f"graph has no OperationData:`{output_name}`")

        # if inputs were provided, remove unnecessary nodes
        necessary_nodes -= unnecessary_nodes

        # get ordered operation steps
        computation_requirements = tuple(step for step in self.ordered_steps if step in necessary_nodes)

        # get required data nodes for computation
        required_inputs = set()
        for node in computation_requirements:
            if isinstance(node, BaseOperation):
                for input_ in node.inputs:
                    if graph.in_degree(input_) == 0:  # type:ignore
                        required_inputs.add(input_)
        required_inputs |= set(inputs)

        # cahche results for future look-up
        required_inputs = tuple(sorted(required_inputs))
        self.cached_requirements[(required_inputs, tuple(outputs))] = (
            required_inputs,
            computation_requirements,
        )

        return required_inputs, computation_requirements

    def __call__(
        self,
        input_dict: Dict,
        outputs: List[str] = [],
        method: CGNetwork.COMPUTE_METHOD = COMPUTE_METHOD.SEQUENTIAL,
    ) -> Any:
        def update_perf_register(step_name: str, step_exec_time: float):
            self.perf_register[step_name] = step_exec_time

        # sourcery skip: default-mutable-arg
        if not self.flag_compiled:
            logging.error("graph not compiled")
            return

        if len(self.ordered_steps) == 0:
            logging.error("no steps after compilation")
            return

        provided_inputs = list(input_dict.keys())
        required_inputs, operation_steps = self.EvaluateComputationRequirements(provided_inputs, outputs)

        if not set(required_inputs).issubset(provided_inputs):
            logging.error(f"Missing required inputs:`{tuple(set(required_inputs) - set(provided_inputs))}`")
            return

        self.perf_register.clear()

        if method == CGNetwork.COMPUTE_METHOD.PARALLEL:
            logging.error("not implemented")
        if method == CGNetwork.COMPUTE_METHOD.DISTRUBUTED:
            logging.error("not implemented")
        elif method == CGNetwork.COMPUTE_METHOD.SEQUENTIAL:
            return sequential_compute(input_dict, outputs, operation_steps, update_perf_register)


def sequential_compute(
    input_dict: Dict[str, Any],
    outputs: List[str],
    operation_steps: Tuple,
    perf_register_callback: Callable[[str, float], None],
) -> Dict[str, Any]:
    cache = dict(input_dict)

    for step in operation_steps:
        if isinstance(step, CGNetwork.ProcessData):
            if step not in cache:
                logging.error(f"missing data:`{step}` in processing stack")
                break

        elif isinstance(step, BaseOperation):
            logging.debug(f"executing opration:`{step}`")
            t_start = time.time()

            temp_outputs = step.Compute(cache)
            cache |= temp_outputs

            perf_register_callback(step.name, time.time() - t_start)

        elif isinstance(step, CGNetwork.DeleteInstruction):
            logging.debug(f"executing opration:`{step}`")
            t_start = time.time()

            cache.pop(step)

            perf_register_callback(step, time.time() - t_start)

    return {k: cache[k] for k in iter(cache) if k in outputs} if outputs else cache
