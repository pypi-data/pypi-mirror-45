# coding=utf-8
# Copyright 2019 The Cirq Developers
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

from __future__ import with_statement
from __future__ import absolute_import
from typing import Sequence

import pytest

import cirq
from itertools import izip


def _assert_equivalent_op_tree(x, y):
    a = list(cirq.flatten_op_tree(x))
    b = list(cirq.flatten_op_tree(y))
    assert a == b


def _assert_equivalent_op_tree_sequence(x,
                                        y):
    assert len(x) == len(y)
    for a, b in izip(x, y):
        _assert_equivalent_op_tree(a, b)


def test_requires_one_override():

    class C(cirq.NoiseModel):
        pass

    with pytest.raises(AssertionError, match=u'override'):
        _ = C()


def test_infers_other_methods():
    q = cirq.LineQubit(0)

    class NoiseModelWithNoisyMomentListMethod(cirq.NoiseModel):

        def noisy_moments(self, moments, system_qubits):
            result = []
            for moment in moments:
                if moment.operations:
                    result.append(cirq.X(moment.operations[0].qubits[0]))
                else:
                    result.append([])
            return result

    a = NoiseModelWithNoisyMomentListMethod()
    _assert_equivalent_op_tree(a.noisy_operation(cirq.H(q)), cirq.X(q))
    _assert_equivalent_op_tree(a.noisy_moment(cirq.Moment([cirq.H(q)]), [q]),
                               cirq.X(q))
    _assert_equivalent_op_tree_sequence(
        a.noisy_moments([cirq.Moment(), cirq.Moment([cirq.H(q)])], [q]),
        [[], cirq.X(q)])

    class NoiseModelWithNoisyMomentMethod(cirq.NoiseModel):

        def noisy_moment(self, moment, system_qubits):
            return cirq.Y.on_each(*moment.qubits)

    b = NoiseModelWithNoisyMomentMethod()
    _assert_equivalent_op_tree(b.noisy_operation(cirq.H(q)), cirq.Y(q))
    _assert_equivalent_op_tree(b.noisy_moment(cirq.Moment([cirq.H(q)]), [q]),
                               cirq.Y(q))
    _assert_equivalent_op_tree_sequence(
        b.noisy_moments([cirq.Moment(), cirq.Moment([cirq.H(q)])], [q]),
        [[], cirq.Y(q)])

    class NoiseModelWithNoisyOperationMethod(cirq.NoiseModel):

        def noisy_operation(self, operation):
            return cirq.Z(operation.qubits[0])

    c = NoiseModelWithNoisyOperationMethod()
    _assert_equivalent_op_tree(c.noisy_operation(cirq.H(q)), cirq.Z(q))
    _assert_equivalent_op_tree(c.noisy_moment(cirq.Moment([cirq.H(q)]), [q]),
                               cirq.Z(q))
    _assert_equivalent_op_tree_sequence(
        c.noisy_moments([cirq.Moment(), cirq.Moment([cirq.H(q)])], [q]),
        [[], cirq.Z(q)])


def test_no_noise():
    q = cirq.LineQubit(0)
    m = cirq.Moment([cirq.X(q)])
    assert cirq.NO_NOISE.noisy_operation(cirq.X(q)) == cirq.X(q)
    assert cirq.NO_NOISE.noisy_moment(m, [q]) is m
    assert cirq.NO_NOISE.noisy_moments([m, m], [q]) == [m, m]
    assert cirq.NO_NOISE == cirq.NO_NOISE
    assert unicode(cirq.NO_NOISE) == u'(no noise)'
    cirq.testing.assert_equivalent_repr(cirq.NO_NOISE)


def test_constant_qubit_noise():
    a, b, c = cirq.LineQubit.range(3)
    damp = cirq.amplitude_damp(0.5)
    damp_all = cirq.ConstantQubitNoiseModel(damp)
    assert damp_all.noisy_moments(
        [cirq.Moment([cirq.X(a)]), cirq.Moment()],
        [a, b, c]) == [[cirq.X(a), damp(a),
                        damp(b), damp(c)], [damp(a), damp(b),
                                            damp(c)]]

    with pytest.raises(ValueError, match=u'num_qubits'):
        _ = cirq.ConstantQubitNoiseModel(cirq.CNOT**0.01)
