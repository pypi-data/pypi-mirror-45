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

u"""Sampling/simulation methods that delegate to appropriate simulators."""

from __future__ import absolute_import
from typing import List, Optional, Type, Union

import numpy as np

from cirq import circuits, protocols, study, schedules
from cirq.sim import sparse_simulator, density_matrix_simulator


def sample(program, **_3to2kwargs):
    if 'dtype' in _3to2kwargs: dtype = _3to2kwargs['dtype']; del _3to2kwargs['dtype']
    else: dtype =  np.complex64
    if 'repetitions' in _3to2kwargs: repetitions = _3to2kwargs['repetitions']; del _3to2kwargs['repetitions']
    else: repetitions =  1
    if 'param_resolver' in _3to2kwargs: param_resolver = _3to2kwargs['param_resolver']; del _3to2kwargs['param_resolver']
    else: param_resolver =  None
    u"""Simulates sampling from the given circuit or schedule.

    Args:
        program: The circuit or schedule to sample from.
        param_resolver: Parameters to run with the program.
        repetitions: The number of samples to take.
        dtype: The `numpy.dtype` used by the simulation. Typically one of
            `numpy.complex64` or `numpy.complex128`.
            Favors speed over precision by default, i.e. uses `numpy.complex64`.
    """

    # State vector simulation is much faster, but only works if no randomness.
    if protocols.has_unitary(program):
        return sparse_simulator.Simulator(dtype=dtype).run(
            program=program,
            param_resolver=param_resolver,
            repetitions=repetitions)

    return density_matrix_simulator.DensityMatrixSimulator(
        dtype=dtype).run(
            program=program,
            param_resolver=param_resolver,
            repetitions=repetitions)


def sample_sweep(program,
                 params, **_3to2kwargs
                 ):
    if 'dtype' in _3to2kwargs: dtype = _3to2kwargs['dtype']; del _3to2kwargs['dtype']
    else: dtype =  np.complex64
    if 'repetitions' in _3to2kwargs: repetitions = _3to2kwargs['repetitions']; del _3to2kwargs['repetitions']
    else: repetitions =  1
    u"""Runs the supplied Circuit or Schedule, mimicking quantum hardware.

    In contrast to run, this allows for sweeping over different parameter
    values.

    Args:
        program: The circuit or schedule to simulate.
        params: Parameters to run with the program.
        repetitions: The number of repetitions to simulate, per set of
            parameter values.
        dtype: The `numpy.dtype` used by the simulation. Typically one of
            `numpy.complex64` or `numpy.complex128`.
            Favors speed over precision by default, i.e. uses `numpy.complex64`.

    Returns:
        TrialResult list for this run; one for each possible parameter
        resolver.
    """
    circuit = (program if isinstance(program, circuits.Circuit)
               else program.to_circuit())
    param_resolvers = study.to_resolvers(params)

    trial_results = []  # type: List[study.TrialResult]
    for param_resolver in param_resolvers:
        measurements = sample(circuit,
                              param_resolver=param_resolver,
                              repetitions=repetitions,
                              dtype=dtype)
        trial_results.append(measurements)
    return trial_results
