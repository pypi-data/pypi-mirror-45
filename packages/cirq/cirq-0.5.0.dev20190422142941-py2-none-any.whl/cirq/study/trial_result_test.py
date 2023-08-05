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
import collections
import numpy as np
import pytest

import cirq


# Python 2 gives a different repr due to unicode strings being prefixed with u.
@cirq.testing.only_test_in_python3
def test_repr():
    v = cirq.TrialResult(
        params=cirq.ParamResolver({u'a': 2}),
        repetitions=2,
        measurements={u'm': np.array([[1, 2]])})

    assert repr(v) == (u"cirq.TrialResult(params=cirq.ParamResolver({'a': 2}), "
                       u"repetitions=2, measurements={'m': array([[1, 2]])})")


def test_str():
    result = cirq.TrialResult(
        params=cirq.ParamResolver({}),
        repetitions=5,
        measurements={
            u'ab': np.array([[0, 1],
                            [0, 1],
                            [0, 1],
                            [1, 0],
                            [0, 1]]),
            u'c': np.array([[0], [0], [1], [0], [1]])
        })
    assert unicode(result) == u'ab=00010, 11101\nc=00101'


def test_histogram():
    result = cirq.TrialResult(
        params=cirq.ParamResolver({}),
        repetitions=5,
        measurements={
            u'ab': np.array([[0, 1],
                            [0, 1],
                            [0, 1],
                            [1, 0],
                            [0, 1]], dtype=np.bool),
            u'c': np.array([[0], [0], [1], [0], [1]], dtype=np.bool)
        })

    assert result.histogram(key=u'ab') == collections.Counter({
        1: 4,
        2: 1
    })
    assert result.histogram(key=u'ab', fold_func=tuple) == collections.Counter({
        (False, True): 4,
        (True, False): 1
    })
    assert result.histogram(key=u'ab',
                            fold_func=lambda e: None) == collections.Counter({
        None: 5,
    })
    assert result.histogram(key=u'c') == collections.Counter({
        0: 3,
        1: 2
    })


def test_multi_measurement_histogram():
    result = cirq.TrialResult(
        params=cirq.ParamResolver({}),
        repetitions=5,
        measurements={
            u'ab': np.array([[0, 1],
                            [0, 1],
                            [0, 1],
                            [1, 0],
                            [0, 1]], dtype=np.bool),
            u'c': np.array([[0], [0], [1], [0], [1]], dtype=np.bool)
        })

    assert result.multi_measurement_histogram(keys=[]) == collections.Counter(
        {(): 5})
    assert (result.multi_measurement_histogram(keys=[u'ab']) ==
            collections.Counter({
                (1,): 4,
                (2,): 1,
            }))
    assert (result.multi_measurement_histogram(keys=[u'c']) ==
            collections.Counter({
                (0,): 3,
                (1,): 2,
            }))
    assert (result.multi_measurement_histogram(keys=[u'ab', u'c']) ==
            collections.Counter({
                (1, 0,): 2,
                (1, 1,): 2,
                (2, 0,): 1,
            }))

    assert result.multi_measurement_histogram(keys=[],
                                              fold_func=lambda e: None
                                              ) == collections.Counter({
        None: 5,
    })
    assert result.multi_measurement_histogram(keys=[u'ab'],
                                              fold_func=lambda e: None
                                              ) == collections.Counter({
        None: 5,
    })
    assert result.multi_measurement_histogram(keys=[u'ab', u'c'],
                                              fold_func=lambda e: None
                                              ) == collections.Counter({
        None: 5,
    })

    assert result.multi_measurement_histogram(keys=[u'ab', u'c'],
                                              fold_func=lambda e: tuple(
                                                  tuple(f) for f in e)
                                              ) == collections.Counter({
        ((False, True), (False,)): 2,
        ((False, True), (True,)): 2,
        ((True, False), (False,)): 1,
    })


def test_trial_result_equality():
    et = cirq.testing.EqualsTester()
    et.add_equality_group(cirq.TrialResult(
        params=cirq.ParamResolver({}),
        repetitions=5,
        measurements={u'a': np.array([[0]])}))
    et.add_equality_group(cirq.TrialResult(
        params=cirq.ParamResolver({}),
        repetitions=6,
        measurements={u'a': np.array([[0]])}))
    et.add_equality_group(cirq.TrialResult(
        params=cirq.ParamResolver({}),
        repetitions=5,
        measurements={u'a': np.array([[1]])}))


def test_qubit_keys_for_histogram():
    a, b, c = cirq.LineQubit.range(3)
    circuit = cirq.Circuit.from_ops(
        cirq.measure(a, b),
        cirq.X(c),
        cirq.measure(c),
    )
    results = cirq.Simulator().run(program=circuit, repetitions=100)
    with pytest.raises(KeyError):
        _ = results.histogram(key=a)

    assert results.histogram(key=[a, b]) == collections.Counter({0: 100})
    assert results.histogram(key=c) == collections.Counter({True: 100})
    assert results.histogram(key=[c]) == collections.Counter({1: 100})


def test_text_diagram_jupyter():
    result = cirq.TrialResult(
        params=cirq.ParamResolver({}),
        repetitions=5,
        measurements={
            u'ab': np.array([[0, 1],
                            [0, 1],
                            [0, 1],
                            [1, 0],
                            [0, 1]], dtype=np.bool),
            u'c': np.array([[0], [0], [1], [0], [1]], dtype=np.bool)
        })

    # Test Jupyter console output from
    class FakePrinter(object):
        def __init__(self):
            self.text_pretty = u''
        def text(self, to_print):
            self.text_pretty += to_print
    p = FakePrinter()
    result._repr_pretty_(p, False)
    assert p.text_pretty == u'ab=00010, 11101\nc=00101'

    # Test cycle handling
    p = FakePrinter()
    result._repr_pretty_(p, True)
    assert p.text_pretty == u'TrialResult(...)'
