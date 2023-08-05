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
from typing import cast, Sequence

from cirq import line, ops, protocols
from cirq.contrib.acquaintance.permutation import (
    PermutationGate, update_mapping)


def assert_permutation_decomposition_equivalence(
        gate,
        n_qubits):
    qubits = line.LineQubit.range(n_qubits)
    operations = protocols.decompose_once_with_qubits(gate, qubits)
    operations = list(
            cast(Sequence[ops.Operation], ops.flatten_op_tree(operations)))
    mapping = dict((cast(ops.Qid, q), i) for i, q in enumerate(qubits))
    update_mapping(mapping, operations)
    expected_mapping = dict((qubits[j], i)
            for i, j in gate.permutation().items())
    assert mapping == expected_mapping, (
        u"{!r}.permutation({}) doesn't match decomposition.\n"
        u'\n'
        u'Actual mapping:\n'
        u'{}\n'
        u'\n'
        u'Expected mapping:\n'
        u'{}\n'.format(gate, n_qubits,
            [mapping[q] for q in qubits],
            [expected_mapping[q] for q in qubits])
    )
