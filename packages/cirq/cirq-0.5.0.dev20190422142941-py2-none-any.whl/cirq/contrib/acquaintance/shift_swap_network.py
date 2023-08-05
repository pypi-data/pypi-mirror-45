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
import functools
import itertools
from typing import Dict, Iterable, Optional, Sequence, Tuple

from cirq import ops, protocols
from cirq.contrib.acquaintance.gates import acquaint
from cirq.contrib.acquaintance.permutation import (
        PermutationGate)
from cirq.contrib.acquaintance.shift import (
        CircularShiftGate)
from itertools import izip


class ShiftSwapNetworkGate(PermutationGate):
    u"""A swap network that generalizes the circular shift gate.

    Given a specification of two partitions, implements a swap network that has
    the overall effect of:
        * For every pair of parts, one from each partition, acquainting the
            union of the corresponding qubits.
        * Circularly shifting the two sets of qubits.

    Args:
        left_part_lens: The sizes of the parts in the partition of the first
            set of qubits.
        right_part_lens: The sizes of the parts in the partition of the second
            set of qubits.
        swap_gate: The gate to use when decomposing.

    Attributes:
        part_lens: A mapping from the side (as a str, 'left' or 'right') to the
            part sizes of the corresponding partition.
        swap_gate: The gate to use when decomposing.
    """

    def __init__(self,
                 left_part_lens,
                 right_part_lens,
                 swap_gate=ops.SWAP
                 ):

        self.part_lens = {
                u'left': tuple(left_part_lens),
                u'right': tuple(right_part_lens)}

        for part_lens in self.part_lens.values():
            if min(part_lens) < 1:
                raise ValueError(u'not min(part_lens)')

        self.swap_gate = swap_gate

    def acquaintance_size(self):
        return sum(max(self.part_lens[side]) for side in (u'left', u'right'))

    def _decompose_(self, qubits):
        part_lens = list(itertools.chain(*(
            self.part_lens[side] for side in (u'left', u'right'))))

        n_qubits = 0
        parts = []
        for part_len in part_lens:
            parts.append(list(qubits[n_qubits: n_qubits + part_len]))
            n_qubits += part_len

        n_parts = len(part_lens)
        n_left_parts = len(self.part_lens[u'left'])
        n_right_parts = n_parts - n_left_parts

        mins = itertools.chain(xrange(n_left_parts - 1, 0, -1),
                               xrange(n_right_parts))
        maxs = itertools.chain(xrange(n_left_parts, n_parts),
                               xrange(n_parts - 1, n_right_parts, -1))
        SHIFT = functools.partial(CircularShiftGate, swap_gate=self.swap_gate)

        for i, j in izip(mins, maxs):
            for k in xrange(i, j, 2):
                left_part, right_part = parts[k: k + 2]
                parts_qubits = left_part + right_part
                yield acquaint(*parts_qubits)
                yield SHIFT(len(parts_qubits), len(left_part))(*parts_qubits)
                parts[k] = parts_qubits[:len(right_part)]
                parts[k + 1] = parts_qubits[len(right_part):]

    def qubit_count(self, side = None):
        if side is None:
            return sum(self.qubit_count(side) for side in self.part_lens)
        return sum(self.part_lens[side])

    def num_qubits(self):
        return self.qubit_count()

    def permutation(self):
        return dict(izip(
            xrange(self.num_qubits()),
            itertools.chain(
                    xrange(self.qubit_count(u'right'), self.num_qubits()),
                    xrange(self.qubit_count(u'right'))
            )))

    def _circuit_diagram_info_(self, args
                               ):
        qubit_count = self.qubit_count()
        assert args.known_qubit_count in (None, qubit_count)

        arrow = u'↦' if args.use_unicode_characters else u'->'

        wire_symbols = []
        for i, side in enumerate((u'left', u'right')):
            for j, part_len in enumerate(self.part_lens[side]):
                for k in xrange(part_len):
                    wire_symbols.append(
                            unicode((i, j, k)) + arrow + unicode((int(not(i)), j, k)))
        return tuple(wire_symbols)

    def __repr__(self):
        args = tuple(repr(self.part_lens[side]) for side in (u'left', u'right'))
        if self.swap_gate != ops.SWAP:
            args += (repr(self.swap_gate),)
        return (u'cirq.contrib.acquaintance.shift_swap_network.'
                u'ShiftSwapNetworkGate' +
                u'({})'.format(u', '.join(args)))

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.part_lens == other.part_lens and
                self.swap_gate == other.swap_gate)
