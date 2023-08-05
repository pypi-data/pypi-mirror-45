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

u"""Tests sampling/simulation methods that delegate to appropriate simulators."""
from __future__ import absolute_import
import collections

import sympy

import cirq


def test_sample():
    q = cirq.NamedQubit(u'q')

    # Unitary.
    results = cirq.sample(cirq.Circuit.from_ops(cirq.X(q), cirq.measure(q)))
    assert results.histogram(key=q) == collections.Counter({1: 1})

    # Intermediate measurements.
    results = cirq.sample(cirq.Circuit.from_ops(
        cirq.measure(q, key=u'drop'),
        cirq.X(q),
        cirq.measure(q),
    ))
    assert results.histogram(key=u'drop') == collections.Counter({0: 1})
    assert results.histogram(key=q) == collections.Counter({1: 1})


def test_sample_sweep():
    q = cirq.NamedQubit(u'q')
    c = cirq.Circuit.from_ops(
        cirq.X(q),
        cirq.Y(q)**sympy.Symbol(u't'),
        cirq.measure(q))

    # Unitary.
    results = cirq.sample_sweep(c, cirq.Linspace(u't', 0, 1, 2), repetitions=3)
    assert len(results) == 2
    assert results[0].histogram(key=q) == collections.Counter({1: 3})
    assert results[1].histogram(key=q) == collections.Counter({0: 3})

    # Overdamped.
    c = cirq.Circuit.from_ops(
        cirq.X(q),
        cirq.amplitude_damp(1).on(q),
        cirq.Y(q)**sympy.Symbol(u't'),
        cirq.measure(q))
    results = cirq.sample_sweep(
        c,
        cirq.Linspace(u't', 0, 1, 2),
        repetitions=3)
    assert len(results) == 2
    assert results[0].histogram(key=q) == collections.Counter({0: 3})
    assert results[1].histogram(key=q) == collections.Counter({1: 3})
