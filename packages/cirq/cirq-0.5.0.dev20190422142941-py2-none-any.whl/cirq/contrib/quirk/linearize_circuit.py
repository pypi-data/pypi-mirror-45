# coding=utf-8
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from typing import Callable

from cirq import ops, circuits, line


class QubitMapper(object):
    def __init__(self, qubit_map
                 ):
        self.qubit_map = qubit_map

    def map_operation(self, operation):
        return operation.transform_qubits(self.qubit_map)

    def map_moment(self, moment):
        return ops.Moment(self.map_operation(op) for op in moment.operations)

    def optimize_circuit(self, circuit):
        circuit[:] = (self.map_moment(m) for m in circuit)


def linearize_circuit_qubits(
        circuit,
        qubit_order = ops.QubitOrder.DEFAULT
        ):
    qubits = ops.QubitOrder.as_qubit_order(qubit_order).order_for(
        circuit.all_qubits())
    qubit_map = dict((q, line.LineQubit(i))
                 for i, q in enumerate(qubits))
    QubitMapper(qubit_map.__getitem__).optimize_circuit(circuit)
