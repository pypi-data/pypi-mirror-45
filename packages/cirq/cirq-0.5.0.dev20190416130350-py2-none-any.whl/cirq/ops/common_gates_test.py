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

from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import
import itertools

import numpy as np
import pytest
import sympy

import cirq


H = np.array([[1, 1], [1, -1]]) * np.sqrt(0.5)
HH = cirq.kron(H, H)
QFT2 = np.array([[1, 1, 1, 1],
                 [1, 1j, -1, -1j],
                 [1, -1, 1, -1],
                 [1, -1j, -1, 1j]]) * 0.5


@pytest.mark.parametrize(u'eigen_gate_type', [
    cirq.CZPowGate,
    cirq.XPowGate,
    cirq.YPowGate,
    cirq.ZPowGate,
])
def test_phase_insensitive_eigen_gates_consistent_protocols(eigen_gate_type):
    cirq.testing.assert_eigengate_implements_consistent_protocols(
            eigen_gate_type)


@pytest.mark.parametrize(u'eigen_gate_type', [
    cirq.CNotPowGate,
    cirq.HPowGate,
    cirq.ISwapPowGate,
    cirq.SwapPowGate,
])
def test_phase_sensitive_eigen_gates_consistent_protocols(eigen_gate_type):
    cirq.testing.assert_eigengate_implements_consistent_protocols(
            eigen_gate_type, ignoring_global_phase=True)

@pytest.mark.parametrize(u'gate_type, num_qubits',
    itertools.product(
        (cirq.MeasurementGate, cirq.IdentityGate),
        xrange(1, 5))
)
def test_consistent_protocols(gate_type, num_qubits):
    gate = gate_type(num_qubits=num_qubits)
    cirq.testing.assert_implements_consistent_protocols(
        gate, qubit_count=num_qubits)


def test_cz_init():
    assert cirq.CZPowGate(exponent=0.5).exponent == 0.5
    assert cirq.CZPowGate(exponent=5).exponent == 5
    assert (cirq.CZ**0.5).exponent == 0.5


def test_cz_str():
    assert unicode(cirq.CZ) == u'CZ'
    assert unicode(cirq.CZ**0.5) == u'CZ**0.5'
    assert unicode(cirq.CZ**-0.25) == u'CZ**-0.25'


def test_cz_repr():
    assert repr(cirq.CZ) == u'cirq.CZ'
    assert repr(cirq.CZ**0.5) == u'(cirq.CZ**0.5)'
    assert repr(cirq.CZ**-0.25) == u'(cirq.CZ**-0.25)'


def test_cz_unitary():
    assert np.allclose(cirq.unitary(cirq.CZ),
                       np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, -1]]))

    assert np.allclose(cirq.unitary(cirq.CZ**0.5),
                       np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1j]]))

    assert np.allclose(cirq.unitary(cirq.CZ**0),
                       np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]]))

    assert np.allclose(cirq.unitary(cirq.CZ**-0.5),
                       np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, -1j]]))


def test_z_init():
    z = cirq.ZPowGate(exponent=5)
    assert z.exponent == 5

    # Canonicalizes exponent for equality, but keeps the inner details.
    assert cirq.Z**0.5 != cirq.Z**-0.5
    assert (cirq.Z**-1)**0.5 == cirq.Z**-0.5
    assert cirq.Z**-1 == cirq.Z


def test_rot_gates_eq():
    eq = cirq.testing.EqualsTester()
    gates = [
        lambda p: cirq.CZ**p,
        lambda p: cirq.X**p,
        lambda p: cirq.Y**p,
        lambda p: cirq.Z**p,
        lambda p: cirq.CNOT**p,
    ]
    for gate in gates:
        eq.add_equality_group(gate(3.5),
                              gate(-0.5))
        eq.make_equality_group(lambda: gate(0))
        eq.make_equality_group(lambda: gate(0.5))

    eq.add_equality_group(cirq.XPowGate(), cirq.XPowGate(exponent=1), cirq.X)
    eq.add_equality_group(cirq.YPowGate(), cirq.YPowGate(exponent=1), cirq.Y)
    eq.add_equality_group(cirq.ZPowGate(), cirq.ZPowGate(exponent=1), cirq.Z)
    eq.add_equality_group(cirq.ZPowGate(exponent=1,
                                        global_shift=-0.5),
                          cirq.ZPowGate(exponent=5,
                                        global_shift=-0.5))
    eq.add_equality_group(cirq.ZPowGate(exponent=3,
                                        global_shift=-0.5))
    eq.add_equality_group(cirq.ZPowGate(exponent=1,
                                        global_shift=-0.1))
    eq.add_equality_group(cirq.ZPowGate(exponent=5,
                                        global_shift=-0.1))
    eq.add_equality_group(cirq.CNotPowGate(),
                          cirq.CNotPowGate(exponent=1),
                          cirq.CNOT)
    eq.add_equality_group(cirq.CZPowGate(),
                          cirq.CZPowGate(exponent=1), cirq.CZ)


def test_z_unitary():
    assert np.allclose(cirq.unitary(cirq.Z),
                       np.array([[1, 0], [0, -1]]))
    assert np.allclose(cirq.unitary(cirq.Z**0.5),
                       np.array([[1, 0], [0, 1j]]))
    assert np.allclose(cirq.unitary(cirq.Z**0),
                       np.array([[1, 0], [0, 1]]))
    assert np.allclose(cirq.unitary(cirq.Z**-0.5),
                       np.array([[1, 0], [0, -1j]]))


def test_y_unitary():
    assert np.allclose(cirq.unitary(cirq.Y),
                       np.array([[0, -1j], [1j, 0]]))

    assert np.allclose(cirq.unitary(cirq.Y**0.5),
                       np.array([[1 + 1j, -1 - 1j], [1 + 1j, 1 + 1j]]) / 2)

    assert np.allclose(cirq.unitary(cirq.Y**0),
                       np.array([[1, 0], [0, 1]]))

    assert np.allclose(cirq.unitary(cirq.Y**-0.5),
                       np.array([[1 - 1j, 1 - 1j], [-1 + 1j, 1 - 1j]]) / 2)


def test_x_unitary():
    assert np.allclose(cirq.unitary(cirq.X),
                       np.array([[0, 1], [1, 0]]))

    assert np.allclose(cirq.unitary(cirq.X**0.5),
                       np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]]) / 2)

    assert np.allclose(cirq.unitary(cirq.X**0),
                       np.array([[1, 0], [0, 1]]))

    assert np.allclose(cirq.unitary(cirq.X**-0.5),
                       np.array([[1 - 1j, 1 + 1j], [1 + 1j, 1 - 1j]]) / 2)


@pytest.mark.parametrize(u'num_qubits', [1, 2, 4])
def test_identity_init(num_qubits):
    assert cirq.IdentityGate(num_qubits).num_qubits() == num_qubits


@pytest.mark.parametrize(u'num_qubits', [1, 2, 4])
def test_identity_unitary(num_qubits):
    i = cirq.IdentityGate(num_qubits)
    assert np.allclose(cirq.unitary(i), np.identity(2 ** num_qubits))


def test_identity_str():
    assert unicode(cirq.IdentityGate(1)) == u'I'
    assert unicode(cirq.IdentityGate(2)) == u'I(2)'


def test_identity_repr():
    assert repr(cirq.IdentityGate(2)) == u'cirq.IdentityGate(2)'


def test_identity_apply_unitary():
    v = np.array([1, 0])
    result = cirq.apply_unitary(
        cirq.I, cirq.ApplyUnitaryArgs(v, np.array([0, 1]), (0,)))
    assert result is v


def test_identity_eq():
    equals_tester = cirq.testing.EqualsTester()
    equals_tester.add_equality_group(cirq.I, cirq.IdentityGate(1))
    equals_tester.add_equality_group(cirq.IdentityGate(2))
    equals_tester.add_equality_group(cirq.IdentityGate(4))


def test_h_unitary():
    sqrt = cirq.unitary(cirq.H**0.5)
    m = np.dot(sqrt, sqrt)
    assert np.allclose(m, cirq.unitary(cirq.H), atol=1e-8)


def test_h_init():
    h = cirq.HPowGate(exponent=0.5)
    assert h.exponent == 0.5


def test_h_str():
    assert unicode(cirq.H) == u'H'
    assert unicode(cirq.H**0.5) == u'H^0.5'


def test_runtime_types_of_rot_gates():
    for gate_type in [lambda p: cirq.CZPowGate(exponent=p),
                      lambda p: cirq.XPowGate(exponent=p),
                      lambda p: cirq.YPowGate(exponent=p),
                      lambda p: cirq.ZPowGate(exponent=p)]:
        p = gate_type(sympy.Symbol(u'a'))
        assert cirq.unitary(p, None) is None
        assert cirq.pow(p, 2, None) == gate_type(2 * sympy.Symbol(u'a'))
        assert cirq.inverse(p, None) == gate_type(-sympy.Symbol(u'a'))

        c = gate_type(0.5)
        assert cirq.unitary(c, None) is not None
        assert cirq.pow(c, 2) == gate_type(1)
        assert cirq.inverse(c) == gate_type(-0.5)


def test_measurement_eq():
    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(cirq.MeasurementGate(1, u''),
                          cirq.MeasurementGate(1, u'', invert_mask=()))
    eq.add_equality_group(cirq.MeasurementGate(1, u'a'))
    eq.add_equality_group(cirq.MeasurementGate(1, u'a', invert_mask=(True,)))
    eq.add_equality_group(cirq.MeasurementGate(1, u'a', invert_mask=(False,)))
    eq.add_equality_group(cirq.MeasurementGate(1, u'b'))
    eq.add_equality_group(cirq.MeasurementGate(2, u'a'))
    eq.add_equality_group(cirq.MeasurementGate(2, u''))
    eq.add_equality_group(cirq.MeasurementGate(3, u'a'))


def test_interchangeable_qubit_eq():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')
    c = cirq.NamedQubit(u'c')
    eq = cirq.testing.EqualsTester()

    eq.add_equality_group(cirq.SWAP(a, b), cirq.SWAP(b, a))
    eq.add_equality_group(cirq.SWAP(a, c))

    eq.add_equality_group(cirq.CZ(a, b), cirq.CZ(b, a))
    eq.add_equality_group(cirq.CZ(a, c))

    eq.add_equality_group(cirq.CNOT(a, b))
    eq.add_equality_group(cirq.CNOT(b, a))
    eq.add_equality_group(cirq.CNOT(a, c))


def test_text_diagrams():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')
    circuit = cirq.Circuit.from_ops(
        cirq.SWAP(a, b),
        cirq.X(a),
        cirq.Y(a),
        cirq.Z(a),
        cirq.Z(a)**sympy.Symbol(u'x'),
        cirq.Rx(sympy.Symbol(u'x')).on(a),
        cirq.CZ(a, b),
        cirq.CNOT(a, b),
        cirq.CNOT(b, a),
        cirq.H(a)**0.5,
        cirq.ISWAP(a, b)**-1,
        cirq.I(a),
        cirq.IdentityGate(2)(a, b))

    cirq.testing.assert_has_diagram(circuit, u"""
a: ───×───X───Y───Z───Z^x───Rx(x)───@───@───X───H^0.5───iSwap──────I───I───
      │                             │   │   │           │              │
b: ───×─────────────────────────────@───X───@───────────iSwap^-1───────I───
""")

    cirq.testing.assert_has_diagram(circuit, u"""
a: ---swap---X---Y---Z---Z^x---Rx(x)---@---@---X---H^0.5---iSwap------I---I---
      |                                |   |   |           |              |
b: ---swap-----------------------------@---X---@-----------iSwap^-1-------I---
""", use_unicode_characters=False)


def test_cnot_unitary():
    np.testing.assert_almost_equal(
        cirq.unitary(cirq.CNOT**0.5),
        np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0.5+0.5j, 0.5-0.5j],
            [0, 0, 0.5-0.5j, 0.5+0.5j],
        ]))


def test_cnot_keyword_arguments():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')

    eq_tester = cirq.testing.EqualsTester()
    eq_tester.add_equality_group(cirq.CNOT(a, b),
                                 cirq.CNOT(control=a, target=b))
    eq_tester.add_equality_group(cirq.CNOT(b, a),
                                 cirq.CNOT(control=b, target=a))


def test_cnot_keyword_not_equal():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')

    with pytest.raises(AssertionError):
        eq_tester = cirq.testing.EqualsTester()
        eq_tester.add_equality_group(cirq.CNOT(a, b),
                                     cirq.CNOT(target=a, control=b))


def test_cnot_keyword_too_few_arguments():
    a = cirq.NamedQubit(u'a')

    with pytest.raises(ValueError):
        _ = cirq.CNOT(control=a)


def test_cnot_mixed_keyword_and_positional_arguments():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')

    with pytest.raises(ValueError):
        _ = cirq.CNOT(a, target=b)


def test_cnot_unknown_keyword_argument():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')

    with pytest.raises(ValueError):
        _ = cirq.CNOT(target=a, controlled=b)


def test_cnot_decompose():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')
    assert cirq.decompose_once(cirq.CNOT(a, b)**sympy.Symbol(u'x')) is not None


def test_swap_unitary():
    np.testing.assert_almost_equal(
        cirq.unitary(cirq.SWAP**0.5),
        np.array([
            [1, 0, 0, 0],
            [0, 0.5 + 0.5j, 0.5 - 0.5j, 0],
            [0, 0.5 - 0.5j, 0.5 + 0.5j, 0],
            [0, 0, 0, 1]
        ]))


def test_repr():
    assert repr(cirq.X) == u'cirq.X'
    assert repr(cirq.X**0.5) == u'(cirq.X**0.5)'

    assert repr(cirq.Z) == u'cirq.Z'
    assert repr(cirq.Z**0.5) == u'cirq.S'
    assert repr(cirq.Z**0.25) == u'cirq.T'
    assert repr(cirq.Z**0.125) == u'(cirq.Z**0.125)'

    assert repr(cirq.S) == u'cirq.S'
    assert repr(cirq.S**-1) == u'(cirq.S**-1)'
    assert repr(cirq.T) == u'cirq.T'
    assert repr(cirq.T**-1) == u'(cirq.T**-1)'

    assert repr(cirq.Y) == u'cirq.Y'
    assert repr(cirq.Y**0.5) == u'(cirq.Y**0.5)'

    assert repr(cirq.I) == u'cirq.I'

    assert repr(cirq.CNOT) == u'cirq.CNOT'
    assert repr(cirq.CNOT**0.5) == u'(cirq.CNOT**0.5)'

    assert repr(cirq.SWAP) == u'cirq.SWAP'
    assert repr(cirq.SWAP ** 0.5) == u'(cirq.SWAP**0.5)'

    assert repr(cirq.ISWAP) == u'cirq.ISWAP'
    assert repr(cirq.ISWAP ** 0.5) == u'(cirq.ISWAP**0.5)'

    cirq.testing.assert_equivalent_repr(
        cirq.X**(sympy.Symbol(u'a') / 2 - sympy.Symbol(u'c') * 3 + 5))

    # There should be no floating point error during initialization, and repr
    # should be using the "shortest decimal value closer to X than any other
    # floating point value" strategy, as opposed to the "exactly value in
    # decimal" strategy.
    assert repr(cirq.CZ**0.2) == u'(cirq.CZ**0.2)'


def test_str():
    assert unicode(cirq.X) == u'X'
    assert unicode(cirq.X**0.5) == u'X**0.5'
    assert unicode(cirq.Rx(np.pi)) == u'Rx(π)'
    assert unicode(cirq.Rx(0.5 * np.pi)) == u'Rx(0.5π)'
    assert unicode(cirq.XPowGate(
        global_shift=-0.25)) == u'XPowGate(exponent=1.0, global_shift=-0.25)'

    assert unicode(cirq.Z) == u'Z'
    assert unicode(cirq.Z**0.5) == u'S'
    assert unicode(cirq.Z**0.125) == u'Z**0.125'
    assert unicode(cirq.Rz(np.pi)) == u'Rz(π)'
    assert unicode(cirq.Rz(1.4 * np.pi)) == u'Rz(1.4π)'
    assert unicode(cirq.ZPowGate(
        global_shift=0.25)) == u'ZPowGate(exponent=1.0, global_shift=0.25)'

    assert unicode(cirq.S) == u'S'
    assert unicode(cirq.S**-1) == u'S**-1'
    assert unicode(cirq.T) == u'T'
    assert unicode(cirq.T**-1) == u'T**-1'

    assert unicode(cirq.Y) == u'Y'
    assert unicode(cirq.Y**0.5) == u'Y**0.5'
    assert unicode(cirq.Ry(np.pi)) == u'Ry(π)'
    assert unicode(cirq.Ry(3.14 * np.pi)) == u'Ry(3.14π)'
    assert unicode(cirq.YPowGate(
        exponent=2,
        global_shift=-0.25)) == u'YPowGate(exponent=2, global_shift=-0.25)'

    assert unicode(cirq.CNOT) == u'CNOT'
    assert unicode(cirq.CNOT**0.5) == u'CNOT**0.5'

    assert unicode(cirq.SWAP) == u'SWAP'
    assert unicode(cirq.SWAP**0.5) == u'SWAP**0.5'

    assert unicode(cirq.ISWAP) == u'ISWAP'
    assert unicode(cirq.ISWAP**0.5) == u'ISWAP**0.5'

def test_measurement_gate_diagram():
    # Shows key.
    assert cirq.circuit_diagram_info(cirq.MeasurementGate(1)
                                     ) == cirq.CircuitDiagramInfo((u"M('')",))
    assert cirq.circuit_diagram_info(
        cirq.MeasurementGate(1, key=u'test')
    ) == cirq.CircuitDiagramInfo((u"M('test')",))

    # Uses known qubit count.
    assert cirq.circuit_diagram_info(
        cirq.MeasurementGate(3),
        cirq.CircuitDiagramInfoArgs(
            known_qubits=None,
            known_qubit_count=3,
            use_unicode_characters=True,
            precision=None,
            qubit_map=None
        )) == cirq.CircuitDiagramInfo((u"M('')", u'M', u'M'))

    # Shows invert mask.
    assert cirq.circuit_diagram_info(
        cirq.MeasurementGate(2, invert_mask=(False, True))
    ) == cirq.CircuitDiagramInfo((u"M('')", u"!M"))

    # Omits key when it is the default.
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')
    cirq.testing.assert_has_diagram(
        cirq.Circuit.from_ops(cirq.measure(a, b)), u"""
a: ───M───
      │
b: ───M───
""")
    cirq.testing.assert_has_diagram(
        cirq.Circuit.from_ops(cirq.measure(a, b, invert_mask=(True,))), u"""
a: ───!M───
      │
b: ───M────
""")
    cirq.testing.assert_has_diagram(
        cirq.Circuit.from_ops(cirq.measure(a, b, key=u'test')), u"""
a: ───M('test')───
      │
b: ───M───────────
""")


def test_measure():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')

    # Empty application.
    with pytest.raises(ValueError, match=u'empty set of qubits'):
        _ = cirq.measure()

    assert cirq.measure(a) == cirq.MeasurementGate(num_qubits=1, key=u'a').on(a)
    assert cirq.measure(a, b) == cirq.MeasurementGate(num_qubits=2,
                                                      key=u'a,b').on(a, b)
    assert cirq.measure(b, a) == cirq.MeasurementGate(num_qubits=2,
                                                      key=u'b,a').on(b, a)
    assert cirq.measure(a, key=u'b') == cirq.MeasurementGate(num_qubits=1,
                                                            key=u'b').on(a)
    assert cirq.measure(a, invert_mask=(True,)) == cirq.MeasurementGate(
        num_qubits=1, key=u'a', invert_mask=(True,)).on(a)

    with pytest.raises(ValueError, match=u'ndarray'):
        _ = cirq.measure(np.ndarray([1, 0]))

    with pytest.raises(ValueError, match=u'Qid'):
        _ = cirq.measure(u"bork")


def test_measurement_channel():
    np.testing.assert_allclose(
            cirq.channel(cirq.MeasurementGate(1)),
            (np.array([[1, 0], [0, 0]]), np.array([[0, 0], [0, 1]])))
    np.testing.assert_allclose(
            cirq.channel(cirq.MeasurementGate(2)),
            (np.array([[1, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]),
             np.array([[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 1]])))


def test_measurement_qubit_count_vs_mask_length():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')
    c = cirq.NamedQubit(u'c')

    _ = cirq.MeasurementGate(num_qubits=1, invert_mask=(True,)).on(a)
    _ = cirq.MeasurementGate(num_qubits=2, invert_mask=(True, False)).on(a, b)
    _ = cirq.MeasurementGate(num_qubits=3, invert_mask=(True, False, True)).on(
        a, b, c)
    with pytest.raises(ValueError):
        _ = cirq.MeasurementGate(num_qubits=1, invert_mask=(True, False)).on(a)
    with pytest.raises(ValueError):
        _ = cirq.MeasurementGate(num_qubits=3,
                                 invert_mask=(True, False, True)).on(a, b)


def test_measure_each():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')

    assert cirq.measure_each() == []
    assert cirq.measure_each(a) == [cirq.measure(a)]
    assert cirq.measure_each(a, b) == [cirq.measure(a), cirq.measure(b)]

    assert cirq.measure_each(a, b, key_func=lambda e: e.name + u'!') == [
        cirq.measure(a, key=u'a!'),
        cirq.measure(b, key=u'b!')
    ]


def test_iswap_str():
    assert unicode(cirq.ISWAP) == u'ISWAP'
    assert unicode(cirq.ISWAP**0.5) == u'ISWAP**0.5'


def test_iswap_unitary():
    cirq.testing.assert_allclose_up_to_global_phase(
        cirq.unitary(cirq.ISWAP),
        np.array([[1, 0, 0, 0],
                  [0, 0, 1j, 0],
                  [0, 1j, 0, 0],
                  [0, 0, 0, 1]]),
        atol=1e-8)


def test_iswap_decompose_diagram():
    a = cirq.NamedQubit(u'a')
    b = cirq.NamedQubit(u'b')

    decomposed = cirq.Circuit.from_ops(
        cirq.decompose_once(cirq.ISWAP(a, b)**0.5))
    cirq.testing.assert_has_diagram(decomposed, u"""
a: ───@───H───X───T───X───T^-1───H───@───
      │       │       │              │
b: ───X───────@───────@──────────────X───
""")


def test_rx_unitary():
    s = np.sqrt(0.5)
    np.testing.assert_allclose(
        cirq.unitary(cirq.Rx(np.pi / 2)),
        np.array([[s, -s*1j], [-s*1j, s]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Rx(-np.pi / 2)),
        np.array([[s, s*1j], [s*1j, s]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Rx(0)),
        np.array([[1, 0], [0, 1]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Rx(2 * np.pi)),
        np.array([[-1, 0], [0, -1]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Rx(np.pi)),
        np.array([[0, -1j], [-1j, 0]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Rx(-np.pi)),
        np.array([[0, 1j], [1j, 0]]))


def test_ry_unitary():
    s = np.sqrt(0.5)
    np.testing.assert_allclose(
        cirq.unitary(cirq.Ry(np.pi / 2)),
        np.array([[s, -s], [s, s]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Ry(-np.pi / 2)),
        np.array([[s, s], [-s, s]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Ry(0)),
        np.array([[1, 0], [0, 1]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Ry(2 * np.pi)),
        np.array([[-1, 0], [0, -1]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Ry(np.pi)),
        np.array([[0, -1], [1, 0]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Ry(-np.pi)),
        np.array([[0, 1], [-1, 0]]))


def test_rz_unitary():
    s = np.sqrt(0.5)
    np.testing.assert_allclose(
        cirq.unitary(cirq.Rz(np.pi / 2)),
        np.array([[s - s*1j, 0], [0, s + s*1j]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Rz(-np.pi / 2)),
        np.array([[s + s*1j, 0], [0, s - s*1j]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Rz(0)),
        np.array([[1, 0], [0, 1]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Rz(2 * np.pi)),
        np.array([[-1, 0], [0, -1]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Rz(np.pi)),
        np.array([[-1j, 0], [0, 1j]]))

    np.testing.assert_allclose(
        cirq.unitary(cirq.Rz(-np.pi)),
        np.array([[1j, 0], [0, -1j]]))


def test_phase_by_xy():
    assert cirq.phase_by(cirq.X, 0.25, 0) == cirq.Y
    assert cirq.phase_by(cirq.Y, 0.25, 0) == cirq.X

    assert cirq.phase_by(cirq.X**0.5, 0.25, 0) == cirq.Y**0.5
    assert cirq.phase_by(cirq.Y**0.5, 0.25, 0) == cirq.X**-0.5
    assert cirq.phase_by(cirq.X**-0.5, 0.25, 0) == cirq.Y**-0.5
    assert cirq.phase_by(cirq.Y**-0.5, 0.25, 0) == cirq.X**0.5


def test_ixyz_circuit_diagram():
    q = cirq.NamedQubit(u'q')
    ix = cirq.XPowGate(exponent=1, global_shift=0.5)
    iy = cirq.YPowGate(exponent=1, global_shift=0.5)
    iz = cirq.ZPowGate(exponent=1, global_shift=0.5)

    cirq.testing.assert_has_diagram(
        cirq.Circuit.from_ops(
            ix(q),
            ix(q)**-1,
            ix(q)**-0.99999,
            ix(q)**-1.00001,
            ix(q)**3,
            ix(q)**4.5,
            ix(q)**4.500001,
        ), u"""
q: ───X───X───X───X───X───X^0.5───X^0.5───
        """)

    cirq.testing.assert_has_diagram(
        cirq.Circuit.from_ops(
            iy(q),
            iy(q)**-1,
            iy(q)**3,
            iy(q)**4.5,
            iy(q)**4.500001,
        ), u"""
q: ───Y───Y───Y───Y^0.5───Y^0.5───
    """)

    cirq.testing.assert_has_diagram(
        cirq.Circuit.from_ops(
            iz(q),
            iz(q)**-1,
            iz(q)**3,
            iz(q)**4.5,
            iz(q)**4.500001,
        ), u"""
q: ───Z───Z───Z───S───S───
    """)


def test_rxyz_circuit_diagram():
    q = cirq.NamedQubit(u'q')

    cirq.testing.assert_has_diagram(
        cirq.Circuit.from_ops(
            cirq.Rx(np.pi).on(q),
            cirq.Rx(-np.pi).on(q),
            cirq.Rx(-np.pi + 0.00001).on(q),
            cirq.Rx(-np.pi - 0.00001).on(q),
            cirq.Rx(3*np.pi).on(q),
            cirq.Rx(7*np.pi/2).on(q),
            cirq.Rx(9*np.pi/2 + 0.00001).on(q),
        ), u"""
q: ───Rx(π)───Rx(-π)───Rx(-π)───Rx(-π)───Rx(-π)───Rx(-0.5π)───Rx(0.5π)───
    """)

    cirq.testing.assert_has_diagram(
        cirq.Circuit.from_ops(
            cirq.Rx(np.pi).on(q),
            cirq.Rx(np.pi/2).on(q),
            cirq.Rx(-np.pi + 0.00001).on(q),
            cirq.Rx(-np.pi - 0.00001).on(q),
        ), u"""
q: ---Rx(pi)---Rx(0.5pi)---Rx(-pi)---Rx(-pi)---
        """,
        use_unicode_characters=False)

    cirq.testing.assert_has_diagram(
        cirq.Circuit.from_ops(
            cirq.Ry(np.pi).on(q),
            cirq.Ry(-np.pi).on(q),
            cirq.Ry(3 * np.pi).on(q),
            cirq.Ry(9*np.pi/2).on(q),
        ), u"""
q: ───Ry(π)───Ry(-π)───Ry(-π)───Ry(0.5π)───
    """)

    cirq.testing.assert_has_diagram(
        cirq.Circuit.from_ops(
            cirq.Rz(np.pi).on(q),
            cirq.Rz(-np.pi).on(q),
            cirq.Rz(3 * np.pi).on(q),
            cirq.Rz(9*np.pi/2).on(q),
            cirq.Rz(9*np.pi/2 + 0.00001).on(q),
        ), u"""
q: ───Rz(π)───Rz(-π)───Rz(-π)───Rz(0.5π)───Rz(0.5π)───
    """)
