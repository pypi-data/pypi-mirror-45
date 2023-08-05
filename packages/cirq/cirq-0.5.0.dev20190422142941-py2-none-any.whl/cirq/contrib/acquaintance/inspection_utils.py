# coding=utf-8
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from typing import FrozenSet, Sequence, Set

from cirq import circuits, devices, ops

from cirq.contrib.acquaintance.executor import (
        AcquaintanceOperation, ExecutionStrategy)
from cirq.contrib.acquaintance.mutation_utils import (
        expose_acquaintance_gates)
from cirq.contrib.acquaintance.permutation import (
        LogicalIndex, LogicalMapping)

class LogicalAnnotator(ExecutionStrategy):
    u"""Realizes acquaintance opportunities.
    """

    def __init__(self,
                 initial_mapping
                 ):
        u"""
        Args:
            initial_mapping: The initial mapping of qubits to logical indices.
        """
        self._initial_mapping = initial_mapping.copy()

    @property
    def initial_mapping(self):
        return self._initial_mapping

    @property
    def device(self):
        return devices.UnconstrainedDevice

    def get_operations(self,
                       indices,
                       qubits
                       ):
        yield AcquaintanceOperation(qubits, indices)


def get_acquaintance_dag(
        strategy,
        initial_mapping
        ):
    strategy = strategy.copy()
    expose_acquaintance_gates(strategy)
    LogicalAnnotator(initial_mapping)(strategy)
    acquaintance_ops = (op for moment in strategy._moments
                        for op in moment.operations
                        if isinstance(op, AcquaintanceOperation))
    return circuits.CircuitDag.from_ops(
            acquaintance_ops, device=strategy.device)


def get_logical_acquaintance_opportunities(
        strategy,
        initial_mapping
        ):
    acquaintance_dag = get_acquaintance_dag(strategy, initial_mapping)
    logical_acquaintance_opportunities = set()
    for op in acquaintance_dag.all_operations():
        logical_acquaintance_opportunities.add(frozenset(op.logical_indices))
    return logical_acquaintance_opportunities
