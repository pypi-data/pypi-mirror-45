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

from __future__ import division
from __future__ import absolute_import
import functools
import itertools
import math
import operator
from typing import Sequence, Dict, Tuple, List, NamedTuple, Optional

from cirq import ops, protocols, value

from cirq.contrib.acquaintance.shift import CircularShiftGate
from cirq.contrib.acquaintance.permutation import (
        PermutationGate, SwapPermutationGate, LinearPermutationGate)
from itertools import izip


def operations_to_part_lens(
        qubit_order,
        op_tree,
        ):
    qubit_sort_key = functools.partial(operator.indexOf, qubit_order)
    op_parts = [tuple(sorted(op.qubits,key=qubit_sort_key))
                for op in ops.flatten_op_tree(op_tree)]
    singletons = [(q,) for q in set(qubit_order).difference(*op_parts)
                 ] # type: List[Tuple[ops.Qid, ...]]
    part_sort_key = lambda p: min(qubit_sort_key(q) for q in p)
    parts = tuple(tuple(part) for part in
                  sorted(singletons + op_parts, key=part_sort_key))

    if sum(parts, ()) != tuple(qubit_order):
        raise ValueError(u'sum(parts, ()) != tuple(qubit_order)')

    return tuple(len(part) for part in parts)


class AcquaintanceOpportunityGate(
        ops.Gate, ops.InterchangeableQubitsGate):
    u"""Represents an acquaintance opportunity. An acquaintance opportunity is
    essentially a placeholder in a swap network that may later be replaced with
    a logical gate."""

    def __init__(self, num_qubits):
        self._num_qubits = num_qubits

    def __repr__(self):
        return (u'cirq.contrib.acquaintance.AcquaintanceOpportunityGate('
                u'num_qubits={!r})'.format(self.num_qubits()))

    def _circuit_diagram_info_(self,
                               args):
        wire_symbol = u'█' if args.use_unicode_characters else u'Acq'
        wire_symbols = (wire_symbol,) * self.num_qubits()
        return wire_symbols

    def num_qubits(self):
        return self._num_qubits


def acquaint(*qubits):
    return AcquaintanceOpportunityGate(len(qubits)).on(*qubits)

Layers = NamedTuple(u'Layers', [
    (u'prior_interstitial', List[ops.Operation]),
    (u'pre', List[ops.Operation]),
    (u'intra', List[ops.Operation]),
    (u'post', List[ops.Operation]),
    (u'posterior_interstitial', List[ops.Operation])
    ])

def new_layers(**kwargs):
    return Layers._make(kwargs.get(field, []) for field in Layers._fields)

def acquaint_insides(swap_gate,
                     acquaintance_gate,
                     qubits,
                     before,
                     layers,
                     mapping
                     ):
    u"""Acquaints each of the qubits with another set specified by an
    acquaintance gate.

    Args:
        qubits: The list of qubits of which half are individually acquainted
            with another list of qubits.
        layers: The layers to put gates into.
        acquaintance_gate: The acquaintance gate that acquaints the end qubit
            with another list of qubits.
        before: Whether the acquainting is done before the shift.
        swap_gate: The gate used to swap logical indices.
        mapping: The mapping from qubits to logical indices. Used to keep track
            of the effect of inside-acquainting swaps.
    """

    max_reach = _get_max_reach(len(qubits), round_up=before)
    reaches = itertools.chain(xrange(1, max_reach + 1),
                    xrange(max_reach, -1, -1))
    offsets = (0, 1) * max_reach
    swap_gate = SwapPermutationGate(swap_gate)
    ops = []
    for offset, reach in izip(offsets, reaches):
        if offset == before:
            ops.append(acquaintance_gate)
        for dr in xrange(offset, reach, 2):
            ops.append(swap_gate(*qubits[dr:dr + 2]))
    intrastitial_layer = getattr(layers, u'pre' if before else u'post')
    intrastitial_layer += ops

    # add interstitial gate
    interstitial_layer = getattr(layers,
            (u'prior' if before else u'posterior') + u'_interstitial')
    interstitial_layer.append(acquaintance_gate)

    # update mapping
    reached_qubits = qubits[:max_reach + 1]
    positions = list(mapping[q] for q in reached_qubits)
    mapping.update(izip(reached_qubits, reversed(positions)))

def _get_max_reach(size, round_up=True):
    if round_up:
        return int(math.ceil(size / 2)) - 1
    return max((size // 2) - 1, 0)


def acquaint_and_shift(parts,
                       layers,
                       acquaintance_size,
                       swap_gate,
                       mapping):
    u"""Acquaints and shifts a pair of lists of qubits. The first part is
    acquainted with every qubit individually in the second part, and vice
    versa. Operations are grouped into several layers:
        * prior_interstitial: The first layer of acquaintance gates.
        * prior: The combination of acquaintance gates and swaps that acquaints
            the inner halves.
        * intra: The shift gate.
        * post: The combination of acquaintance gates and swaps that acquaints
            the outer halves.
        * posterior_interstitial: The last layer of acquaintance gates.

    Args:
        parts: The two lists of qubits to acquaint.
        layers: The layers to put gates into.
        acquaintance_size: The number of qubits to acquaint at a time. If None,
            after each pair of parts is shifted the union thereof is
            acquainted.
        swap_gate: The gate used to swap logical indices.
        mapping: The mapping from qubits to logical indices. Used to keep track
            of the effect of inside-acquainting swaps.
    """
    left_part, right_part = parts
    left_size, right_size = len(left_part), len(right_part)
    assert not (set(left_part) & set(right_part))
    qubits = left_part + right_part
    shift = CircularShiftGate(len(qubits),
                              left_size,
                              swap_gate=swap_gate)(
                                      *qubits)
    if acquaintance_size is None:
        layers.intra.append(shift)
        layers.post.append(acquaint(*qubits))
        shift.gate.update_mapping(mapping, qubits)
    elif max(left_size, right_size) != acquaintance_size - 1:
        layers.intra.append(shift)
        shift.gate.update_mapping(mapping, qubits)
    elif acquaintance_size == 2:
        layers.prior_interstitial.append(acquaint(*qubits))
        layers.intra.append(shift)
        shift.gate.update_mapping(mapping, qubits)
    else:
        # before
        if left_size == acquaintance_size - 1:
            # right part
            pre_acquaintance_gate = acquaint(*qubits[:acquaintance_size])
            acquaint_insides(
                    swap_gate=swap_gate,
                    acquaintance_gate=pre_acquaintance_gate,
                    qubits=right_part,
                    before=True,
                    layers=layers,
                    mapping=mapping)

        if right_size == acquaintance_size - 1:
            # left part
            pre_acquaintance_gate = acquaint(*qubits[-acquaintance_size:])
            acquaint_insides(
                    swap_gate=swap_gate,
                    acquaintance_gate=pre_acquaintance_gate,
                    qubits=left_part[::-1],
                    before=True,
                    layers=layers,
                    mapping=mapping)

        layers.intra.append(shift)
        shift.gate.update_mapping(mapping, qubits)

        # after
        if ((left_size == acquaintance_size - 1) and
            (right_size > 1)):
            # right part
            post_acquaintance_gate = acquaint(*qubits[-acquaintance_size:])

            new_left_part = qubits[right_size - 1::-1]
            acquaint_insides(
                    swap_gate=swap_gate,
                    acquaintance_gate=post_acquaintance_gate,
                    qubits=new_left_part,
                    before=False,
                    layers=layers,
                    mapping=mapping)

        if ((right_size == acquaintance_size - 1) and
            (left_size > 1)):
            # left part

            post_acquaintance_gate = acquaint(*qubits[:acquaintance_size])
            acquaint_insides(
                    swap_gate=swap_gate,
                    acquaintance_gate=post_acquaintance_gate,
                    qubits=qubits[right_size:],
                    before=False,
                    layers=layers,
                    mapping=mapping)


class SwapNetworkGate(PermutationGate):
    u"""A single gate representing a generalized swap network.

    Args:
        part_lens: An sequence indicating the sizes of the parts in the
            partition defining the swap network.
        acquaintance_size: An int indicating the locality of the logical gates
            desired; used to keep track of this while nesting. If 0, no
            acquaintance gates are inserted. If None, after each pair of parts
            is shifted the union thereof is acquainted.
        swap_gate: The gate used to swap logical indices.

    Attributes:
        part_lens: See above.
        acquaintance_size: See above.
        swap_gate: The gate used to swap logical indices.
    """

    def __init__(self,
                 part_lens,
                 acquaintance_size=0,
                 swap_gate=ops.SWAP
                 ):
        super(SwapNetworkGate, self).__init__(sum(part_lens), swap_gate)
        if len(part_lens) < 2:
            raise ValueError(u'len(part_lens) < 2.')
        self.part_lens = tuple(part_lens)
        self.acquaintance_size = acquaintance_size

    def _decompose_(self, qubits):
        qubit_to_position = dict((q, i) for i, q in enumerate(qubits))
        mapping = dict(qubit_to_position)
        parts = []
        n_qubits = 0
        for part_len in self.part_lens:
            parts.append(list(qubits[n_qubits: n_qubits + part_len]))
            n_qubits += part_len
        n_parts = len(parts)
        op_sort_key = (None if self.acquaintance_size is None else
                (lambda op:
                qubit_to_position[min(op.qubits, key=qubit_to_position.get)] %
                self.acquaintance_size))
        layers = new_layers()
        for layer_num in xrange(n_parts):
            layers = new_layers(
                    prior_interstitial=layers.posterior_interstitial)
            for i in xrange(layer_num % 2, n_parts - 1, 2):
                left_part, right_part = parts[i:i+2]
                acquaint_and_shift(parts=(left_part, right_part),
                                   layers=layers,
                                   acquaintance_size=self.acquaintance_size,
                                   swap_gate=self.swap_gate,
                                   mapping=mapping)

                parts_qubits = list(left_part + right_part)
                parts[i] = parts_qubits[:len(right_part)]
                parts[i + 1] = parts_qubits[len(right_part):]
            layers.prior_interstitial.sort(key=op_sort_key)
            for l in (u'prior_interstitial', u'pre', u'intra', u'post'):
                yield getattr(layers, l)
        layers.posterior_interstitial.sort(key=op_sort_key)
        yield layers.posterior_interstitial

        assert list(itertools.chain(*(
            sorted(mapping[q] for q in part) for part in reversed(parts)))
            ) == range(n_qubits)

        # finish reversal
        final_permutation = dict((i, n_qubits - 1 - mapping[q])
                for i, q in enumerate(qubits))
        final_gate = LinearPermutationGate(
                n_qubits, final_permutation, self.swap_gate)
        if final_gate:
            yield final_gate(*qubits)

    def _circuit_diagram_info_(self,
                               args):
        wire_symbol = (u'×' if args.use_unicode_characters else u'swap')
        wire_symbols = tuple(
            wire_symbol + u'({},{})'.format(part_index, qubit_index)
            for part_index, part_len in enumerate(self.part_lens)
            for qubit_index in xrange(part_len))
        return protocols.CircuitDiagramInfo(
            wire_symbols=wire_symbols)

    @staticmethod
    def from_operations(qubit_order,
                        operations,
                        acquaintance_size = 0,
                        swap_gate=ops.SWAP
                        ):
        part_sizes = operations_to_part_lens(qubit_order, operations)
        return SwapNetworkGate(part_sizes, acquaintance_size)

    def permutation(self):
        return dict((i, j) for i, j in
                enumerate(reversed(xrange(sum(self.part_lens)))))

    def __repr__(self):
        return (u'cirq.contrib.acquaintance.SwapNetworkGate('
                u'{!r}, {!r})'.format(self.part_lens, self.acquaintance_size))

    def _value_equality_values_(self):
        return (self.part_lens, self.acquaintance_size, self.swap_gate)

SwapNetworkGate = value.value_equality(SwapNetworkGate)
