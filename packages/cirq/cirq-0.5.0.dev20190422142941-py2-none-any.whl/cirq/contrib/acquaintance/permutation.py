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
from typing import Dict, Sequence, Tuple, TypeVar, Union

import abc

from cirq import circuits, ops, optimizers, protocols, value
from itertools import izip


LogicalIndex = TypeVar(u'LogicalIndex', int, ops.Qid)
LogicalIndexSequence = Union[Sequence[int], Sequence[ops.Qid]]
LogicalGates = Dict[Tuple[LogicalIndex, ...], ops.Gate]
LogicalMappingKey = TypeVar(u'LogicalMappingKey', bound=ops.Qid)
LogicalMapping = Dict[LogicalMappingKey, LogicalIndex]


class PermutationGate(ops.Gate):
    __metaclass__ = abc.ABCMeta
    u"""A permutation gate indicates a change in the mapping from qubits to
    logical indices.

    Args:
        swap_gate: the gate that swaps the indices mapped to by a pair of
            qubits (e.g. SWAP or fermionic swap).
    """

    def __init__(self, num_qubits, swap_gate=ops.SWAP):
        self._num_qubits = num_qubits
        self.swap_gate = swap_gate

    def num_qubits(self):
        return self._num_qubits

    @abc.abstractmethod
    def permutation(self):
        u"""permutation = {i: s[i]} indicates that the i-th element is mapped to
        the s[i]-th element."""

    def update_mapping(self, mapping,
                       keys
                       ):
        u"""Updates a mapping (in place) from qubits to logical indices.

        Args:
            mapping: The mapping to update.
            keys: The qubits acted on by the gate.
        """
        permutation = self.permutation()
        indices = tuple(permutation.keys())
        new_keys = [keys[permutation[i]] for i in indices]
        old_elements = [mapping[keys[i]] for i in indices]
        mapping.update(izip(new_keys, old_elements))

    @staticmethod
    def validate_permutation(permutation,
                             n_elements=None):
        if not permutation:
            return
        if set(permutation.values()) != set(permutation):
            raise IndexError(u'key and value sets must be the same.')
        if min(permutation) < 0:
            raise IndexError(u'keys of the permutation must be non-negative.')
        if n_elements is not None:
            if max(permutation) >= n_elements:
                raise IndexError(u'key is out of bounds.')

    def _circuit_diagram_info_(self, args
                               ):
        if args.known_qubit_count is None:
            return NotImplemented
        permutation = self.permutation()
        arrow = u'↦' if args.use_unicode_characters else u'->'
        wire_symbols = tuple(unicode(i) + arrow + unicode(permutation.get(i, i))
                        for i in xrange(self.num_qubits()))
        return wire_symbols


class SwapPermutationGate(PermutationGate):
    u"""Generic swap gate."""

    def __init__(self, swap_gate=ops.SWAP):
        super(SwapPermutationGate, self).__init__(2, swap_gate)

    def permutation(self):
        return {0: 1, 1: 0}

    def _decompose_(
            self, qubits):
        yield self.swap_gate(*qubits)


def _canonicalize_permutation(permutation):
    return dict((i, j) for i, j in permutation.items() if i != j)


class LinearPermutationGate(PermutationGate):
    u"""A permutation gate that decomposes a given permutation using a linear
        sorting network."""

    def __init__(self,
                 num_qubits,
                 permutation,
                 swap_gate=ops.SWAP
                 ):
        u"""Initializes a linear permutation gate.

        Args:
            permutation: The permutation effected by the gate.
            swap_gate: The swap gate used in decompositions.
        """
        super(LinearPermutationGate, self).__init__(num_qubits, swap_gate)
        PermutationGate.validate_permutation(permutation, num_qubits)
        self._permutation = permutation

    def permutation(self):
        return self._permutation

    def _decompose_(self, qubits):
        swap_gate = SwapPermutationGate(self.swap_gate)
        n_qubits = len(qubits)
        mapping = dict((i, self._permutation.get(i, i)) for i in xrange(n_qubits))
        for layer_index in xrange(n_qubits):
            for i in xrange(layer_index % 2, n_qubits - 1, 2):
                if mapping[i] > mapping[i + 1]:
                    yield swap_gate(*qubits[i:i+2])
                    mapping[i], mapping[i+1] = mapping[i+1], mapping[i]

    def __repr__(self):
        return (u'cirq.contrib.acquaintance.LinearPermutationGate('
                u'{!r}, {!r}, {!r})'.format(
                self.num_qubits(), self._permutation, self.swap_gate))

    def _value_equality_values_(self):
        return (tuple(sorted((i, j) for i, j in self._permutation.items()
                if i != j)), self.swap_gate)

    def __nonzero__(self):
        return bool(_canonicalize_permutation(self._permutation))

    def __pow__(self, exponent):
        if exponent == 1:
            return self
        if exponent == -1:
            return LinearPermutationGate(
                self._num_qubits, dict((v, k) for k, v in self._permutation.items()),
                self.swap_gate)
        return NotImplemented


LinearPermutationGate = value.value_equality(unhashable=True)(LinearPermutationGate)

def update_mapping(mapping,
                   operations
                   ):
    u"""Updates a mapping (in place) from qubits to logical indices according to
    a set of permutation gates. Any gates other than permutation gates are
    ignored.

    Args:
        mapping: The mapping to update.
        operations: The operations to update according to.
    """
    for op in ops.flatten_op_tree(operations):
        if (isinstance(op, ops.GateOperation) and
            isinstance(op.gate, PermutationGate)):
            op.gate.update_mapping(mapping, op.qubits)


class ExpandPermutationGates(optimizers.ExpandComposite):
    u"""Decomposes any permutation gates other SwapPermutationGate."""
    def __init__(self):
        circuits.PointOptimizer.__init__(self)

        self.no_decomp = lambda op: (not all(
                [isinstance(op, ops.GateOperation),
                 isinstance(op.gate, PermutationGate),
                 not isinstance(op.gate, SwapPermutationGate)]))

expand_permutation_gates = ExpandPermutationGates()
