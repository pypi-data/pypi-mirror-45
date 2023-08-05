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

u"""A simplified time-slice of operations within a sequenced circuit."""

from __future__ import absolute_import
from typing import Any, Callable, Iterable, Sequence, TypeVar, Union

from cirq.protocols import approx_eq
from cirq.ops import raw_types

TSelf_Moment = TypeVar(u'TSelf_Moment', bound=u'Moment')


class Moment(object):
    u"""A simplified time-slice of operations within a sequenced circuit.

    Note that grouping sequenced circuits into moments is an abstraction that
    may not carry over directly to the scheduling on the hardware or simulator.
    Operations in the same moment may or may not actually end up scheduled to
    occur at the same time. However the topological quantum circuit ordering
    will be preserved, and many schedulers or consumers will attempt to
    maximize the moment representation.

    Attributes:
        operations: A tuple of the Operations for this Moment.
        qubits: A set of the qubits acted upon by this Moment.
    """

    def __init__(self, operations = ()):
        u"""Constructs a moment with the given operations.

        Args:
            operations: The operations applied within the moment.
                Will be frozen into a tuple before storing.

        Raises:
            ValueError: A qubit appears more than once.
        """
        self.operations = tuple(operations)

        # Check that operations don't overlap.
        affected_qubits = [q for op in self.operations for q in op.qubits]
        self.qubits = frozenset(affected_qubits)
        if len(affected_qubits) != len(self.qubits):
            raise ValueError(
                u'Overlapping operations: {}'.format(self.operations))

    def operates_on_single_qubit(self, qubit):
        u"""Determines if the moment has operations touching the given qubit.
        Args:
            qubit: The qubit that may or may not be touched by operations.
        Returns:
            Whether this moment has operations involving the qubit.
        """
        return qubit in self.qubits

    def operates_on(self, qubits):
        u"""Determines if the moment has operations touching the given qubits.

        Args:
            qubits: The qubits that may or may not be touched by operations.

        Returns:
            Whether this moment has operations involving the qubits.
        """
        return any(q in qubits for q in self.qubits)

    def with_operation(self, operation):
        u"""Returns an equal moment, but with the given op added.

        Args:
            operation: The operation to append.

        Returns:
            The new moment.
        """
        return Moment(self.operations + (operation,))

    def without_operations_touching(self, qubits):
        u"""Returns an equal moment, but without ops on the given qubits.

        Args:
            qubits: Operations that touch these will be removed.

        Returns:
            The new moment.
        """
        qubits = frozenset(qubits)
        if not self.operates_on(qubits):
            return self
        return Moment(
            operation for operation in self.operations
            if qubits.isdisjoint(frozenset(operation.qubits)))

    def __copy__(self):
        return type(self)(self.operations)

    def __nonzero__(self):
        return bool(self.operations)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.operations == other.operations

    def _approx_eq_(self, other, atol):
        u"""See `cirq.protocols.SupportsApproximateEquality`."""
        if not isinstance(other, type(self)):
            return NotImplemented
        return approx_eq(self.operations, other.operations, atol=atol)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((Moment, self.operations))

    def __iter__(self):
        return iter(self.operations)

    def __len__(self):
        return len(self.operations)

    def __repr__(self):
        if not self.operations:
            return u'cirq.Moment()'
        return u'cirq.Moment(operations={})'.format(
            _list_repr_with_indented_item_lines(self.operations))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u' and '.join(unicode(op) for op in self.operations)

    def transform_qubits(self,
                         func
                         ):
        return self.__class__(op.transform_qubits(func)
                for op in self.operations)


def _list_repr_with_indented_item_lines(items):
    block = u'\n'.join([repr(op) + u',' for op in items])
    indented = u'    ' + u'\n    '.join(block.split(u'\n'))
    return u'[\n{}\n]'.format(indented)
