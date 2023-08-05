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
from typing import (
    Dict, Iterable, Optional, Union, cast
)

import sympy

from cirq import ops, value, study, protocols
from cirq.contrib.paulistring.pauli_string_raw_types import (
    PauliStringGateOperation)
from cirq.ops.pauli_string import PauliString


class PauliStringPhasor(PauliStringGateOperation):
    u"""An operation that phases a Pauli string."""
    def __init__(self,
                 pauli_string, **_3to2kwargs):
        if 'degs' in _3to2kwargs: degs = _3to2kwargs['degs']; del _3to2kwargs['degs']
        else: degs =  None
        if 'rads' in _3to2kwargs: rads = _3to2kwargs['rads']; del _3to2kwargs['rads']
        else: rads =  None
        if 'half_turns' in _3to2kwargs: half_turns = _3to2kwargs['half_turns']; del _3to2kwargs['half_turns']
        else: half_turns =  None
        u"""Initializes the operation.

        At most one angle argument may be specified. If more are specified,
        the result is considered ambiguous and an error is thrown. If no angle
        argument is given, the default value of one half turn is used.

        If pauli_string is negative, the sign is transferred to the phase.

        Args:
            pauli_string: The PauliString to phase.
            half_turns: Phasing of the Pauli string, in half_turns.
            rads: Phasing of the Pauli string, in radians.
            degs: Phasing of the Pauli string, in degrees.
        """
        half_turns = value.chosen_angle_to_half_turns(
                            half_turns=half_turns,
                            rads=rads,
                            degs=degs)
        if not protocols.is_parameterized(half_turns):
            half_turns = 1 - (1 - half_turns) % 2
        super(PauliStringPhasor, self).__init__(pauli_string)
        self.half_turns = half_turns

    def _value_equality_values_(self):
        return self.pauli_string, self.half_turns

    def map_qubits(self, qubit_map):
        ps = self.pauli_string.map_qubits(qubit_map)
        return PauliStringPhasor(ps, half_turns=self.half_turns)

    def _with_half_turns(self, half_turns
                         ):
        return PauliStringPhasor(self.pauli_string, half_turns=half_turns)

    def __pow__(self,
                exponent):
        new_exponent = protocols.mul(self.half_turns, exponent, NotImplemented)
        if new_exponent is NotImplemented:
            return NotImplemented
        return self._with_half_turns(new_exponent)

    def can_merge_with(self, op):
        return self.pauli_string.equal_up_to_coefficient(op.pauli_string)

    def merged_with(self, op):
        if not self.can_merge_with(op):
            raise ValueError(u'Cannot merge operations: {}, {}'.format(self, op))
        coef = op.pauli_string.coefficient * self.pauli_string.coefficient
        if coef not in [-1, 1]:
            raise NotImplementedError(u"TODO: merge phased pauli operations.")
        half_turns = (cast(float, self.half_turns)
                      + cast(float, op.half_turns) * int(coef.real))
        return PauliStringPhasor(self.pauli_string, half_turns=half_turns)

    def _decompose_(self):
        if len(self.pauli_string) <= 0:
            return
        if self.pauli_string.coefficient not in [-1, +1]:
            raise NotImplementedError(u"TODO: arbitrary coefficients.")
        qubits = self.qubits
        any_qubit = qubits[0]
        to_z_ops = ops.freeze_op_tree(self.pauli_string.to_z_basis_ops())
        xor_decomp = tuple(xor_nonlocal_decompose(qubits, any_qubit))
        yield to_z_ops
        yield xor_decomp
        sign = self.pauli_string.coefficient.real
        yield ops.Z(any_qubit)**protocols.mul(self.half_turns, sign)
        yield protocols.inverse(xor_decomp)
        yield protocols.inverse(to_z_ops)

    def _circuit_diagram_info_(self, args
                               ):
        return self._pauli_string_diagram_info(args,
                                               exponent=self.half_turns,
                                               exponent_absorbs_sign=True)

    def _trace_distance_bound_(self):
        return protocols.trace_distance_bound(ops.Z**self.half_turns)

    def _is_parameterized_(self):
        return protocols.is_parameterized(self.half_turns)

    def _resolve_parameters_(self, param_resolver
                                    ):
        return self._with_half_turns(
                        param_resolver.value_of(self.half_turns))

    def pass_operations_over(self,
                             ops,
                             after_to_before = False
                             ):
        new_pauli_string = self.pauli_string.pass_operations_over(
                                    ops, after_to_before)
        return PauliStringPhasor(new_pauli_string, half_turns=self.half_turns)

    def __repr__(self):
        return u'PauliStringPhasor({!r}, half_turns={!r})'.format(
                    self.pauli_string, self.half_turns)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'({})**{}'.format(self.pauli_string, self.half_turns)


PauliStringPhasor = value.value_equality(PauliStringPhasor)

def xor_nonlocal_decompose(qubits,
                           onto_qubit):
    u"""Decomposition ignores connectivity."""
    for qubit in qubits:
        if qubit != onto_qubit:
            yield ops.CNOT(qubit, onto_qubit)
