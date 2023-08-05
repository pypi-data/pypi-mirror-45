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
from typing import Dict, Iterable, Union, Callable

import sympy

from cirq import value, protocols
from cirq.ops import (raw_types, common_gates, pauli_string as ps, pauli_gates,
                      op_tree, pauli_string_raw_types)


class PauliStringPhasor(pauli_string_raw_types.PauliStringGateOperation):
    u"""An operation that phases the eigenstates of a Pauli string.

    The -1 eigenstates of the Pauli string will have their amplitude multiplied
    by e^(i pi exponent_neg) while +1 eigenstates of the Pauli string will have
    their amplitude multiplied by e^(i pi exponent_pos).
    """

    def __init__(self,
                 pauli_string, **_3to2kwargs):
        if 'exponent_pos' in _3to2kwargs: exponent_pos = _3to2kwargs['exponent_pos']; del _3to2kwargs['exponent_pos']
        else: exponent_pos =  0
        if 'exponent_neg' in _3to2kwargs: exponent_neg = _3to2kwargs['exponent_neg']; del _3to2kwargs['exponent_neg']
        else: exponent_neg =  1
        u"""Initializes the operation.

        Args:
            pauli_string: The PauliString defining the positive and negative
                eigenspaces that will be independently phased.
            exponent_neg: How much to phase vectors in the negative eigenspace,
                in the form of the t in (-1)**t = exp(i pi t).
            exponent_pos: How much to phase vectors in the positive eigenspace,
                in the form of the t in (-1)**t = exp(i pi t).
        """
        if pauli_string.coefficient == -1:
            pauli_string = -pauli_string
            exponent_pos, exponent_neg = exponent_neg, exponent_pos

        if pauli_string.coefficient != 1:
            raise ValueError(
                u"Given PauliString doesn't have +1 and -1 eigenvalues. "
                u"pauli_string.coefficient must be 1 or -1.")

        super(PauliStringPhasor, self).__init__(pauli_string)
        self.exponent_neg = value.canonicalize_half_turns(exponent_neg)
        self.exponent_pos = value.canonicalize_half_turns(exponent_pos)

    @property
    def exponent_relative(self):
        return value.canonicalize_half_turns(self.exponent_neg -
                                             self.exponent_pos)

    def _value_equality_values_(self):
        return (
            self.pauli_string,
            self.exponent_neg,
            self.exponent_pos,
        )

    def equal_up_to_global_phase(self, other):
        if isinstance(other, PauliStringPhasor):
            rel1 = self.exponent_relative
            rel2 = other.exponent_relative
            return rel1 == rel2 and self.pauli_string == other.pauli_string
        return False

    def map_qubits(self, qubit_map):
        return PauliStringPhasor(self.pauli_string.map_qubits(qubit_map),
                                 exponent_neg=self.exponent_neg,
                                 exponent_pos=self.exponent_pos)

    def __pow__(self,
                exponent):
        pn = protocols.mul(self.exponent_neg, exponent, None)
        pp = protocols.mul(self.exponent_pos, exponent, None)
        if pn is None or pp is None:
            return NotImplemented
        return PauliStringPhasor(self.pauli_string,
                                 exponent_neg=pn,
                                 exponent_pos=pp)

    def can_merge_with(self, op):
        return self.pauli_string.equal_up_to_coefficient(op.pauli_string)

    def merged_with(self, op):
        if not self.can_merge_with(op):
            raise ValueError(u'Cannot merge operations: {}, {}'.format(self, op))
        pp = self.exponent_pos + op.exponent_pos
        pn = self.exponent_neg + op.exponent_neg
        return PauliStringPhasor(self.pauli_string,
                                 exponent_pos=pp,
                                 exponent_neg=pn)

    def _decompose_(self):
        if len(self.pauli_string) <= 0:
            return
        qubits = self.qubits
        any_qubit = qubits[0]
        to_z_ops = op_tree.freeze_op_tree(self.pauli_string.to_z_basis_ops())
        xor_decomp = tuple(xor_nonlocal_decompose(qubits, any_qubit))
        yield to_z_ops
        yield xor_decomp

        if self.exponent_neg:
            yield pauli_gates.Z(any_qubit)**self.exponent_neg
        if self.exponent_pos:
            yield pauli_gates.X(any_qubit)
            yield pauli_gates.Z(any_qubit)**self.exponent_pos
            yield pauli_gates.X(any_qubit)

        yield protocols.inverse(xor_decomp)
        yield protocols.inverse(to_z_ops)

    def _circuit_diagram_info_(self, args
                              ):
        return self._pauli_string_diagram_info(args,
                                               exponent=self.exponent_relative)

    def _trace_distance_bound_(self):
        return protocols.trace_distance_bound(
            pauli_gates.Z**self.exponent_relative)

    def _is_parameterized_(self):
        return (protocols.is_parameterized(self.exponent_neg) or
                protocols.is_parameterized(self.exponent_pos))

    def _resolve_parameters_(self, param_resolver):
        return PauliStringPhasor(
            self.pauli_string,
            exponent_neg=param_resolver.value_of(self.exponent_neg),
            exponent_pos=param_resolver.value_of(self.exponent_pos))

    def pass_operations_over(self,
                             ops,
                             after_to_before = False
                            ):
        new_pauli_string = self.pauli_string.pass_operations_over(
            ops, after_to_before)
        pp = self.exponent_pos
        pn = self.exponent_neg
        return PauliStringPhasor(new_pauli_string,
                                 exponent_pos=pp,
                                 exponent_neg=pn)

    def __repr__(self):
        return (u'cirq.PauliStringPhasor({!r}, '
                u'exponent_neg={!r}, '
                u'exponent_pos={!r})'.format(self.pauli_string,
                                            self.exponent_neg,
                                            self.exponent_pos))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self.exponent_pos == -self.exponent_neg:
            return u'exp({}iπ{}*{})'.format(
                u'-' if self.exponent_pos < 0 else u'',
                u'' if abs(self.exponent_relative) == 1 else abs(
                    self.exponent_pos * 2), self.pauli_string)
        return u'({})**{}'.format(self.pauli_string, self.exponent_relative)


PauliStringPhasor = value.value_equality(approximate=True)(PauliStringPhasor)

def xor_nonlocal_decompose(qubits,
                           onto_qubit
                          ):
    u"""Decomposition ignores connectivity."""
    for qubit in qubits:
        if qubit != onto_qubit:
            yield common_gates.CNOT(qubit, onto_qubit)
