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

u"""Classes to represent displays.

A Display is an operation that signifies extracting some information about the
qubits it is applied to without actually performing any effect on those qubits.
Each Display in a circuit has an associated key, and the result of computing
the values of Displays in a circuit is a dictionary from Display key to
Display value.
"""

from __future__ import absolute_import
from typing import Any, Dict, Hashable, Optional, Tuple, Union, TYPE_CHECKING

import abc

import numpy as np

from cirq import protocols, value
from cirq.ops import op_tree, raw_types

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from cirq.ops import pauli_string


class SamplesDisplay(raw_types.Operation):
    u"""A display whose value is computed from measurement results.

    The value of a SamplesDisplay on some qubits is computed in the following
    steps:
        1. Repeat the following some number of times:
            a. Start with the state which exists just prior to the Moment
               containing the SamplesDisplay
            b. Perform some unitary operations on the qubits
            c. Sample a bitstring from the resulting state
        2. Apply a function to the sampled bitstrings
    """

    @property
    @abc.abstractmethod
    def key(self):
        pass

    @abc.abstractmethod
    def measurement_basis_change(self):
        u"""Operations to perform prior to measurement."""

    @property
    @abc.abstractmethod
    def num_samples(self):
        u"""The number of measurement samples to take."""

    @abc.abstractmethod
    def value_derived_from_samples(self,
                                   measurements):
        u"""The value of the display, derived from measurement samples.

        Args:
            measurements: A 2-dimensional numpy array storing measurement
                results. The first dimension corresponds to the sample and
                the second to the actual boolean measurement results, ordered
                by the qubits that were measured. Therefore, the array has
                shape (self.num_samples, len(self.qubits))

        Returns:
            The value of the display.
        """


class WaveFunctionDisplay(raw_types.Operation):
    u"""A display whose value is computed from the full wavefunction."""

    @property
    @abc.abstractmethod
    def key(self):
        pass

    @abc.abstractmethod
    def value_derived_from_wavefunction(self,
                                        state,
                                        qubit_map
                                        ):
        u"""The value of the display, derived from the full wavefunction.

        Args:
            state: The wavefunction.
            qubit_map: A dictionary from qubit to qubit index in the
                ordering used to define the wavefunction.
        """


class DensityMatrixDisplay(WaveFunctionDisplay):
    u"""A display whose value is computed from the density matrix."""

    @abc.abstractmethod
    def value_derived_from_density_matrix(self,
                                          state,
                                          qubit_map
                                          ):
        u"""The value of the display, derived from the density matrix.

        Args:
            state: The density matrix.
            qubit_map: A dictionary from qubit to qubit index in the
                ordering used to define the wavefunction.
        """

    def value_derived_from_wavefunction(self,
                                        state,
                                        qubit_map
                                        ):
        density_matrix = np.outer(state, np.conj(state))
        return self.value_derived_from_density_matrix(density_matrix, qubit_map)


class ApproxPauliStringExpectation(SamplesDisplay):
    u"""Approximate expectation value of a Pauli string."""

    def __init__(self,
                 pauli_string,
                 num_samples,
                 key=u''):
        self._pauli_string = pauli_string
        self._num_samples = num_samples
        self._key = key

    @property
    def qubits(self):
        return self._pauli_string.qubits

    def with_qubits(self,
                    *new_qubits
                    ):
        return ApproxPauliStringExpectation(
                self._pauli_string.with_qubits(*new_qubits),
                self._num_samples,
                self._key
        )

    @property
    def key(self):
        return self._key

    def measurement_basis_change(self):
        return self._pauli_string.to_z_basis_ops()

    @property
    def num_samples(self):
        return self._num_samples

    def value_derived_from_samples(self,
                                   measurements):
        return np.mean([(-1)**np.sum(bitstring) for bitstring in measurements])

    def _value_equality_values_(self):
        return self._pauli_string, self._num_samples, self._key


ApproxPauliStringExpectation = value.value_equality(ApproxPauliStringExpectation)

class PauliStringExpectation(DensityMatrixDisplay):
    u"""Expectation value of a Pauli string."""

    def __init__(self,
                 pauli_string,
                 key=u''):
        self._pauli_string = pauli_string
        self._key = key

    @property
    def qubits(self):
        return self._pauli_string.qubits

    def with_qubits(self,
                    *new_qubits
                    ):
        return PauliStringExpectation(
                self._pauli_string.with_qubits(*new_qubits),
                self._key
        )

    @property
    def key(self):
        return self._key

    def value_derived_from_wavefunction(self,
                                        state,
                                        qubit_map
                                        ):
        num_qubits = state.shape[0].bit_length() - 1
        ket = np.reshape(np.copy(state), (2,) * num_qubits)
        for qubit, pauli in self._pauli_string.items():
            buffer = np.empty(ket.shape, dtype=state.dtype)
            args = protocols.ApplyUnitaryArgs(
                    target_tensor=ket,
                    available_buffer=buffer,
                    axes=(qubit_map[qubit],)
                    )
            ket = protocols.apply_unitary(pauli, args)
        ket = np.reshape(ket, state.shape)
        return np.dot(state.conj(), ket)

    def value_derived_from_density_matrix(self,
                                          state,
                                          qubit_map
                                          ):
        num_qubits = state.shape[0].bit_length() - 1
        result = np.reshape(np.copy(state), (2,) * num_qubits * 2)
        for qubit, pauli in self._pauli_string.items():
            buffer = np.empty(result.shape, dtype=state.dtype)
            args = protocols.ApplyUnitaryArgs(
                    target_tensor=result,
                    available_buffer=buffer,
                    axes=(qubit_map[qubit],)
                    )
            result = protocols.apply_unitary(pauli, args)
        result = np.reshape(result, state.shape)
        return np.trace(result)

    def _value_equality_values_(self):
        return self._pauli_string, self._key


PauliStringExpectation = value.value_equality(PauliStringExpectation)

def pauli_string_expectation(
        pauli_string,
        num_samples = None,
        key=u''):
    if num_samples is None:
        return PauliStringExpectation(pauli_string, key=key)
    return ApproxPauliStringExpectation(pauli_string, num_samples, key=key)
