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
from __future__ import absolute_import
import pytest

import cirq
import cirq.neutral_atoms as neutral_atoms


def square_device(width, height, holes=(),
                  max_controls=2):
    us = cirq.Duration(nanos=10**3)
    ms = cirq.Duration(nanos=10**6)
    return neutral_atoms.NeutralAtomDevice(measurement_duration=50 * ms,
                              gate_duration=100 * us,
                              control_radius=1.5,
                              max_parallel_z=3,
                              max_parallel_xy=3,
                              max_parallel_c=max_controls,
                              qubits=[cirq.GridQubit(row, col)
                              for col in xrange(width)
                              for row in xrange(height)
                              if cirq.GridQubit(row, col) not in holes])


def test_init():
    d = square_device(2, 2, holes=[cirq.GridQubit(1, 1)])
    us = cirq.Duration(nanos=10 ** 3)
    ms = cirq.Duration(nanos=10 ** 6)
    q00 = cirq.GridQubit(0, 0)
    q01 = cirq.GridQubit(0, 1)
    q10 = cirq.GridQubit(1, 0)

    assert d.qubits == set([q10, q00, q01])
    assert d.duration_of(cirq.GateOperation(
        cirq.IdentityGate(1), [q00])) == 100 * us
    assert d.duration_of(cirq.measure(q00)) == 50 * ms
    with pytest.raises(ValueError):
        _ = d.duration_of(cirq.SingleQubitGate().on(q00))


def test_init_errors():
    line = cirq.LineQubit.range(3)
    us = cirq.Duration(nanos=10 ** 3)
    ms = cirq.Duration(nanos=10 ** 6)
    with pytest.raises(ValueError, match=u"Unsupported qubit type"):
        _ = neutral_atoms.NeutralAtomDevice(measurement_duration=50 * ms,
                               gate_duration=100 * us,
                               control_radius=1.5,
                               max_parallel_z=3,
                               max_parallel_xy=3,
                               max_parallel_c=3,
                               qubits= line)
    with pytest.raises(ValueError, match=u"max_parallel_c must be less"):
        _ = neutral_atoms.NeutralAtomDevice(measurement_duration=50 * ms,
                               gate_duration=100 * us,
                               control_radius=1.5,
                               max_parallel_z=3,
                               max_parallel_xy=3,
                               max_parallel_c=4,
                               qubits= [cirq.GridQubit(0,0)])


def test_decompose_error():
    d = square_device(2, 2, holes=[cirq.GridQubit(1, 1)])
    for op in d.decompose_operation((cirq.CCZ**1.5).on(*(d.qubit_list()))):
        d.validate_operation(op)


def test_validate_gate_errors():
    d = square_device(1,1)

    d.validate_gate(cirq.IdentityGate(4))
    with pytest.raises(ValueError, match=u"controlled gates must have integer "
                       u"exponents"):
        d.validate_gate(cirq.CNotPowGate(exponent=0.5))
    with pytest.raises(ValueError, match=u"Unsupported gate"):
        d.validate_gate(cirq.SingleQubitGate())


def test_validate_operation_errors():
    d = square_device(3, 3)

    class bad_op(cirq.Operation):

        def bad_op(self):
            pass

        def qubits(self):
            pass

        def with_qubits(self, new_qubits):
            pass

    with pytest.raises(ValueError, match=u"Unsupported operation"):
        d.validate_operation(bad_op())
    not_on_device_op = cirq.ParallelGateOperation(cirq.X,
                                                  [cirq.GridQubit(row, col)
                                                   for col in xrange(4)
                                                   for row in xrange(4)])
    with pytest.raises(ValueError, match=u"Qubit not on device"):
        d.validate_operation(not_on_device_op)
    with pytest.raises(ValueError, match=u"Too many qubits acted on in parallel "
                       u"by"):
        d.validate_operation(cirq.CCX.on(*d.qubit_list()[0:3]))
    with pytest.raises(ValueError, match=u"are too far away"):
        d.validate_operation(cirq.CZ.on(cirq.GridQubit(0, 0),
                                        cirq.GridQubit(2, 2)))
    with pytest.raises(ValueError, match=u"Too many Z gates in parallel"):
        d.validate_operation(cirq.ParallelGateOperation(cirq.Z, d.qubits))
    with pytest.raises(ValueError, match=u"Bad number of XY gates in parallel"):
        d.validate_operation(cirq.ParallelGateOperation(cirq.X,
                                                        d.qubit_list()[1:]))


def test_validate_moment_errors():
    d = square_device(3, 3)
    q00 = cirq.GridQubit(0, 0)
    q01 = cirq.GridQubit(0, 1)
    q10 = cirq.GridQubit(1, 0)
    q11 = cirq.GridQubit(1, 1)
    q12 = cirq.GridQubit(1, 2)
    q02 = cirq.GridQubit(0, 2)
    q04 = cirq.GridQubit(0, 4)
    q03 = cirq.GridQubit(0, 3)
    q20 = cirq.GridQubit(2, 0)
    q21 = cirq.GridQubit(2, 1)

    m = cirq.Moment([cirq.Z.on(q00), (cirq.Z**2).on(q01)])
    with pytest.raises(ValueError, match=u"Non-identical simultaneous "):
        d.validate_moment(m)
    m = cirq.Moment([cirq.X.on(q00), cirq.Y.on(q01)])
    with pytest.raises(ValueError, match=u"Non-identical simultaneous "):
        d.validate_moment(m)
    m = cirq.Moment([cirq.CNOT.on(q00, q01), cirq.CZ.on(q12, q02)])
    with pytest.raises(ValueError, match=u"Non-identical simultaneous "):
        d.validate_moment(m)
    m = cirq.Moment([cirq.CNOT.on(q00, q01), cirq.CNOT.on(q12, q02)])
    with pytest.raises(ValueError, match=u"Too many qubits acted on by "
                       u"controlled gates"):
        d.validate_moment(m)
    m = cirq.Moment([cirq.CNOT.on(q00, q01), cirq.Z.on(q02)])
    with pytest.raises(ValueError, match=u"Can't perform non-controlled "
                       u"operations at same time as controlled operations"):
        d.validate_moment(m)
    m = cirq.Moment(cirq.Z.on_each(*d.qubits))
    with pytest.raises(ValueError, match=u"Too many simultaneous Z gates"):
        d.validate_moment(m)
    m = cirq.Moment(cirq.X.on_each(*(d.qubit_list()[1:])))
    with pytest.raises(ValueError, match=u"Bad number of simultaneous XY gates"):
        d.validate_moment(m)
    m = cirq.Moment([cirq.MeasurementGate(1).on(q00), cirq.Z.on(q01)])
    with pytest.raises(ValueError, match=u"Measurements can't be simultaneous "
                       u"with other operations"):
        d.validate_moment(m)
    d.validate_moment(cirq.Moment([cirq.X.on(q00), cirq.Z.on(q01)]))
    us = cirq.Duration(nanos=10 ** 3)
    ms = cirq.Duration(nanos=10 ** 6)
    d2 = neutral_atoms.NeutralAtomDevice(measurement_duration=50 * ms,
                              gate_duration=100 * us,
                              control_radius=1.5,
                              max_parallel_z=4,
                              max_parallel_xy=4,
                              max_parallel_c=4,
                              qubits=[cirq.GridQubit(row, col)
                              for col in xrange(2)
                              for row in xrange(2)])
    m = cirq.Moment([cirq.CNOT.on(q00, q01), cirq.CNOT.on(q10, q11)])
    with pytest.raises(ValueError, match=u"Interacting controlled operations"):
        d2.validate_moment(m)
    d2 = neutral_atoms.NeutralAtomDevice(measurement_duration=50 * ms,
                              gate_duration=100 * us,
                              control_radius=1.1,
                              max_parallel_z=6,
                              max_parallel_xy=6,
                              max_parallel_c=6,
                              qubits=[cirq.GridQubit(row, col)
                              for col in xrange(5)
                              for row in xrange(5)])
    m = cirq.Moment([cirq.CZ.on(q00, q01),
                     cirq.CZ.on(q03, q04), cirq.CZ.on(q20, q21)])
    d2.validate_moment(m)
    m = cirq.Moment([cirq.CZ.on(q00, q01),
                     cirq.CZ.on(q02, q03), cirq.CZ.on(q10, q11)])
    with pytest.raises(ValueError, match=u"Interacting controlled operations"):
        d2.validate_moment(m)


def test_can_add_operation_into_moment_coverage():
    d = square_device(2, 2)
    q00 = cirq.GridQubit(0, 0)
    q01 = cirq.GridQubit(0, 1)
    q10 = cirq.GridQubit(1, 0)
    m = cirq.Moment([cirq.X.on(q00)])
    assert not d.can_add_operation_into_moment(cirq.X.on(q00), m)
    assert not d.can_add_operation_into_moment(cirq.CZ.on(q01, q10), m)
    assert d.can_add_operation_into_moment(cirq.Z.on(q01), m)


def test_validate_circuit_errors():
    d = square_device(2, 2, max_controls=3)
    q00 = cirq.GridQubit(0, 0)
    q01 = cirq.GridQubit(0, 1)
    q10 = cirq.GridQubit(1, 0)
    q11 = cirq.GridQubit(1, 1)
    c = cirq.Circuit()
    c.append(cirq.ParallelGateOperation(cirq.X, d.qubits))
    c.append(cirq.CCZ.on(q00, q01, q10))
    c.append(cirq.ParallelGateOperation(cirq.Z, [q00, q01, q10]))
    m = cirq.Moment(cirq.X.on_each(q00, q01) + cirq.Z.on_each(q10, q11))
    c.append(m)
    c.append(cirq.measure_each(*d.qubits))
    d.validate_circuit(c)
    c.append(cirq.Moment([cirq.X.on(q00)]))
    with pytest.raises(ValueError, match=u"Non-empty moment after measurement"):
        d.validate_circuit(c)


def test_validate_scheduled_operation_errors():
    d = square_device(2, 2)
    s = cirq.Schedule(device=cirq.UnconstrainedDevice)
    q00 = cirq.GridQubit(0, 0)
    so = cirq.ScheduledOperation(cirq.Timestamp(), cirq.Duration(nanos=1),
                                 cirq.X.on(q00))
    with pytest.raises(ValueError, match=u"Incompatible operation duration"):
        d.validate_scheduled_operation(s, so)


def test_validate_schedule_errors():
    d = square_device(2, 2, max_controls=3)
    s = cirq.Schedule(device=cirq.UnconstrainedDevice)
    q00 = cirq.GridQubit(0, 0)
    q01 = cirq.GridQubit(0, 1)
    q10 = cirq.GridQubit(1, 0)
    q11 = cirq.GridQubit(1, 1)
    us = cirq.Duration(nanos=10**3)
    ms = cirq.Duration(nanos=10**6)
    msone = cirq.Timestamp(nanos=10**6)
    mstwo = cirq.Timestamp(nanos=2*10**6)
    msthree = cirq.Timestamp(nanos=3*10**6)
    for qubit in d.qubits:
        s.include(cirq.ScheduledOperation(cirq.Timestamp(nanos=0), 100*us,
                                          cirq.X.on(qubit)))
    s.include(cirq.ScheduledOperation(msone, 100*us,
                                      cirq.TOFFOLI.on(q00,q01,q10)))
    s.include(cirq.ScheduledOperation(mstwo, 100*us, cirq.ParallelGateOperation(
        cirq.X, [q00, q01])))
    s.include(cirq.ScheduledOperation(mstwo, 100*us, cirq.ParallelGateOperation(
        cirq.Z, [q10, q11])))
    for qubit in d.qubits:
        s.include(cirq.ScheduledOperation(msthree,
                                          50*ms,
                                          cirq.GateOperation(
                                              cirq.MeasurementGate(1, qubit),
                                              [qubit])))
    d.validate_schedule(s)
    s.include(cirq.ScheduledOperation(cirq.Timestamp(nanos=10**9), 100*us,
                                      cirq.X.on(q00)))
    with pytest.raises(ValueError, match=u"Non-measurement operation after "
                       u"measurement"):
        d.validate_schedule(s)


def test_repr():
    d = square_device(1, 1)
    cirq.testing.assert_equivalent_repr(d)


def test_str():
    assert unicode(square_device(2, 2)).strip() == u"""
(0, 0)───(0, 1)
│        │
│        │
(1, 0)───(1, 1)
    """.strip()
