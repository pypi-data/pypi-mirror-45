# coding=utf-8
# Copyright 2018 The ops Developers
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
from typing import Sequence

from cirq import ops, circuits, optimizers
from cirq.contrib.paulistring.pauli_string_optimize import (
    pauli_string_optimized_circuit)
from cirq.contrib.paulistring.clifford_optimize import (
    clifford_optimized_circuit)


def optimized_circuit(circuit,
                      atol = 1e-8,
                      repeat = 10,
                      merge_interactions = True
                      ):
    circuit = circuits.Circuit(circuit)  # Make a copy
    for _ in xrange(repeat):
        start_len = len(circuit)
        start_cz_count = _cz_count(circuit)
        if merge_interactions:
            optimizers.MergeInteractions(allow_partial_czs=False,
                                         post_clean_up=_optimized_ops,
                                         ).optimize_circuit(circuit)
        circuit2 = pauli_string_optimized_circuit(
                        circuit,
                        move_cliffords=False,
                        atol=atol)
        circuit3 = clifford_optimized_circuit(
                        circuit2,
                        atol=atol)
        if (len(circuit3) == start_len
            and _cz_count(circuit3) == start_cz_count):
            return circuit3
        circuit = circuit3
    return circuit


def _optimized_ops(ops,
                   atol = 1e-8,
                   repeat = 10):
    c = circuits.Circuit.from_ops(ops)
    c_opt = optimized_circuit(c, atol, repeat, merge_interactions=False)
    return c_opt.all_operations()


def _cz_count(circuit):
    return sum(isinstance(op, ops.GateOperation)
               and isinstance(op, ops.CZPowGate)
               for op in circuit)
