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

from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import
import numpy as np
import pytest

import cirq


@pytest.mark.parametrize(u'keys, coefficient, terms_expected', (
    ((), 10, {}),
    ((u'X',), 2, {u'X': 2}),
    ((u'a', u'b', u'c', u'd'), 0.5, {u'a': 0.5, u'b': 0.5, u'c': 0.5, u'd': 0.5}),
    ((u'b', u'c', u'd', u'e'), -2j, {u'b': -2j, u'c': -2j, u'd': -2j, u'e': -2j}),
))
def test_fromkeys(keys, coefficient, terms_expected):
    actual = cirq.LinearDict.fromkeys(keys, coefficient)
    expected = cirq.LinearDict(terms_expected)
    assert actual == expected
    assert expected == actual


@pytest.mark.parametrize(u'terms, valid_vectors, invalid_vectors', (
    ({u'X': 2}, (u'X'), (u'A', u'B')),
    ({u'X': 2, u'Y': -2}, (u'X', u'Y', u'Z'), (u'A', u'B')),
))
def test_invalid_vectors_are_rejected(terms, valid_vectors, invalid_vectors):
    linear_dict = cirq.LinearDict(terms, validator=lambda v: v in valid_vectors)

    with pytest.raises(ValueError):
        linear_dict += cirq.LinearDict.fromkeys(invalid_vectors, 1)
    assert linear_dict == cirq.LinearDict(terms)

    for vector in invalid_vectors:
        with pytest.raises(ValueError):
            linear_dict[vector] += 1
    assert linear_dict == cirq.LinearDict(terms)

    with pytest.raises(ValueError):
        linear_dict.update(cirq.LinearDict.fromkeys(invalid_vectors, 1))
    assert linear_dict == cirq.LinearDict(terms)


@pytest.mark.parametrize(u'terms, valid_vectors', (
    ({u'X': 2}, (u'X')),
    ({u'X': 2, u'Y': -2}, (u'X', u'Y', u'Z')),
))
def test_valid_vectors_are_accepted(terms, valid_vectors):
    linear_dict = cirq.LinearDict(terms, validator=lambda v: v in valid_vectors)

    original_dict = linear_dict.copy()
    delta_dict = cirq.LinearDict.fromkeys(valid_vectors, 1)

    linear_dict += cirq.LinearDict.fromkeys(valid_vectors, 1)
    assert linear_dict == original_dict + delta_dict

    for vector in valid_vectors:
        linear_dict[vector] += 1
    assert linear_dict == original_dict + 2 * delta_dict

    linear_dict.update(cirq.LinearDict.fromkeys(valid_vectors, 1))
    assert linear_dict == delta_dict


@pytest.mark.parametrize(u'terms, atol, terms_expected', (
    ({u'X': 1, u'Y': 2, u'Z': 3}, 2, {u'Z': 3}),
    ({u'X': 0.1, u'Y': 1, u'Z': 10}, 1e-3, {u'X': 0.1, u'Y': 1, u'Z': 10}),
    ({u'X': 1e-10, u'H': 1e-11}, 1e-9, {}),
    ({}, 1, {}),
))
def test_clean(terms, atol, terms_expected):
    linear_dict = cirq.LinearDict(terms)
    linear_dict.clean(atol=atol)
    expected = cirq.LinearDict(terms_expected)
    assert linear_dict == expected
    assert expected == linear_dict


@pytest.mark.parametrize(u'terms', (
    {u'X': 1j/2}, {u'X': 1, u'Y': 2, u'Z': 3}, {},
))
def test_copy(terms):
    original = cirq.LinearDict(terms)
    copy = original.copy()
    assert type(copy) == cirq.LinearDict
    assert copy == original
    assert original == copy
    original[u'a'] = 1
    assert copy != original
    assert original != copy
    assert u'a' in original
    assert u'a' not in copy


@pytest.mark.parametrize(u'terms, expected_keys', (
    ({}, ()),
    ({u'X': 0}, ()),
    ({u'X': 0.1}, (u'X',)),
    ({u'X': -1, u'Y': 0, u'Z': 1}, (u'X', u'Z')),
))
def test_keys(terms, expected_keys):
    linear_dict = cirq.LinearDict(terms)
    assert tuple(sorted(linear_dict.keys())) == expected_keys


@pytest.mark.parametrize(u'terms, expected_values', (
    ({}, ()),
    ({u'X': 0}, ()),
    ({u'X': 0.1}, (0.1,)),
    ({u'X': -1, u'Y': 0, u'Z': 1}, (-1, 1)),
))
def test_values(terms, expected_values):
    linear_dict = cirq.LinearDict(terms)
    assert tuple(sorted(linear_dict.values())) == expected_values


@pytest.mark.parametrize(u'terms, expected_items', (
    ({}, ()),
    ({u'X': 0}, ()),
    ({u'X': 0.1}, ((u'X', 0.1),)),
    ({u'X': -1, u'Y': 0, u'Z': 1}, ((u'X', -1), (u'Z', 1))),
))
def test_items(terms, expected_items):
    linear_dict = cirq.LinearDict(terms)
    assert tuple(sorted(linear_dict.items())) == expected_items


@pytest.mark.parametrize(u'terms_1, terms_2, terms_expected', (
    ({}, {}, {}),
    ({}, {u'X': 0.1}, {u'X': 0.1}),
    ({u'X': 1}, {u'Y': 2}, {u'X': 1, u'Y': 2}),
    ({u'X': 1}, {u'X': 4}, {u'X': 4}),
    ({u'X': 1, u'Y': 2}, {u'Y': -2}, {u'X': 1, u'Y': -2}),
))
def test_update(terms_1, terms_2, terms_expected):
    linear_dict_1 = cirq.LinearDict(terms_1)
    linear_dict_2 = cirq.LinearDict(terms_2)
    linear_dict_1.update(linear_dict_2)
    expected = cirq.LinearDict(terms_expected)
    assert linear_dict_1 == expected
    assert expected == linear_dict_1


@pytest.mark.parametrize(u'terms, vector, expected_coefficient', (
    ({}, u'', 0),
    ({}, u'X', 0),
    ({u'X': 0}, u'X', 0),
    ({u'X': -1j}, u'X', -1j),
    ({u'X': 1j}, u'Y', 0),
))
def test_get(terms, vector, expected_coefficient):
    linear_dict = cirq.LinearDict(terms)
    actual_coefficient = linear_dict.get(vector)
    assert actual_coefficient == expected_coefficient


@pytest.mark.parametrize(u'terms, vector, expected', (
    ({}, u'X', False),
    ({u'X': 0}, u'X', False),
    ({u'X': 0.1}, u'X', True),
    ({u'X': 1, u'Y': -1}, u'Y', True),
))
def test_contains(terms, vector, expected):
    linear_dict = cirq.LinearDict(terms)
    actual = vector in linear_dict
    assert actual == expected


@pytest.mark.parametrize(u'terms, vector, expected_coefficient', (
    ({}, u'X', 0),
    ({u'X': 1}, u'X', 1),
    ({u'Y': 1}, u'X', 0),
    ({u'X': 2, u'Y': 3}, u'X', 2),
    ({u'X': 1, u'Y': 2}, u'Z', 0),
))
def test_getitem(terms, vector, expected_coefficient):
    linear_dict = cirq.LinearDict(terms)
    actual_coefficient = linear_dict[vector]
    assert actual_coefficient == expected_coefficient


@pytest.mark.parametrize(u'terms, vector, coefficient, terms_expected', (
    ({}, u'X', 0, {}),
    ({}, u'X', 1, {u'X': 1}),
    ({u'X': 1}, u'X', 2, {u'X': 2}),
    ({u'X': 1, u'Y': 3}, u'X', 2, {u'X': 2, u'Y': 3}),
    ({u'X': 1, u'Y': 2}, u'X', 0, {u'Y': 2}),
))
def test_setitem(terms, vector, coefficient, terms_expected):
    linear_dict = cirq.LinearDict(terms)
    linear_dict[vector] = coefficient
    expected = cirq.LinearDict(terms_expected)
    assert linear_dict == expected
    assert expected == linear_dict


@pytest.mark.parametrize(u'terms, vector, terms_expected', (
    ({}, u'X', {}),
    ({u'X': 1}, u'X', {}),
    ({u'X': 1}, u'Y', {u'X': 1}),
    ({u'X': 1, u'Y': 3}, u'X', {u'Y': 3}),
))
def test_delitem(terms, vector, terms_expected):
    linear_dict = cirq.LinearDict(terms)
    del linear_dict[vector]
    expected = cirq.LinearDict(terms_expected)
    assert linear_dict == expected
    assert expected == linear_dict


def test_addition_in_iteration():
    linear_dict = cirq.LinearDict({u'a': 2, u'b': 1, u'c': 0, u'd': -1, u'e': -2})
    for v in linear_dict:
        linear_dict[v] += 1
    assert linear_dict == cirq.LinearDict(
        {u'a': 3, u'b': 2, u'c': 0, u'd': 0, u'e': -1})
    assert linear_dict == cirq.LinearDict({u'a': 3, u'b': 2, u'e': -1})


def test_multiplication_in_iteration():
    linear_dict = cirq.LinearDict({u'u': 2, u'v': 1, u'w': -1})
    for v, c in linear_dict.items():
        if c > 0:
            linear_dict[v] *= 0
    assert linear_dict == cirq.LinearDict({u'u': 0, u'v': 0, u'w': -1})
    assert linear_dict == cirq.LinearDict({u'w': -1})


@pytest.mark.parametrize(u'terms, expected_length', (
    ({}, 0),
    ({u'X': 0}, 0),
    ({u'X': 0.1}, 1),
    ({u'X': 1, u'Y': -2j}, 2),
    ({u'X': 0, u'Y': 1}, 1)
))
def test_len(terms, expected_length):
    linear_dict = cirq.LinearDict(terms)
    assert len(linear_dict) == expected_length


@pytest.mark.parametrize(u'terms_1, terms_2, terms_expected', (
    ({}, {}, {}),
    ({}, {u'X': 0.1}, {u'X': 0.1}),
    ({u'X': 1}, {u'Y': 2}, {u'X': 1, u'Y': 2}),
    ({u'X': 1}, {u'X': 1}, {u'X': 2}),
    ({u'X': 1, u'Y': 2}, {u'Y': -2}, {u'X': 1}),
))
def test_vector_addition(terms_1, terms_2, terms_expected):
    linear_dict_1 = cirq.LinearDict(terms_1)
    linear_dict_2 = cirq.LinearDict(terms_2)
    actual_1 = linear_dict_1 + linear_dict_2
    actual_2 = linear_dict_1
    actual_2 += linear_dict_2
    expected = cirq.LinearDict(terms_expected)
    assert actual_1 == expected
    assert actual_2 == expected
    assert actual_1 == actual_2


@pytest.mark.parametrize(u'terms_1, terms_2, terms_expected', (
    ({}, {}, {}),
    ({u'a': 2}, {u'a': 2}, {}),
    ({u'a': 3}, {u'a': 2}, {u'a': 1}),
    ({u'X': 1}, {u'Y': 2}, {u'X': 1, u'Y': -2}),
    ({u'X': 1}, {u'X': 1}, {}),
    ({u'X': 1, u'Y': 2}, {u'Y': 2}, {u'X': 1}),
    ({u'X': 1, u'Y': 2}, {u'Y': 3}, {u'X': 1, u'Y': -1}),
))
def test_vector_subtraction(terms_1, terms_2, terms_expected):
    linear_dict_1 = cirq.LinearDict(terms_1)
    linear_dict_2 = cirq.LinearDict(terms_2)
    actual_1 = linear_dict_1 - linear_dict_2
    actual_2 = linear_dict_1
    actual_2 -= linear_dict_2
    expected = cirq.LinearDict(terms_expected)
    assert actual_1 == expected
    assert actual_2 == expected
    assert actual_1 == actual_2


@pytest.mark.parametrize(u'terms, terms_expected', (
    ({}, {}),
    ({u'key': 1}, {u'key': -1}),
    ({u'1': 10, u'2': -20}, {u'1': -10, u'2': 20}),
))
def test_vector_negation(terms, terms_expected):
    linear_dict = cirq.LinearDict(terms)
    actual = -linear_dict
    expected = cirq.LinearDict(terms_expected)
    assert actual == expected
    assert expected == actual


@pytest.mark.parametrize(u'scalar, terms, terms_expected', (
    (2, {}, {}),
    (2, {u'X': 1, u'Y': -2}, {u'X': 2, u'Y': -4}),
    (0, {u'abc': 10, u'def': 20}, {}),
    (1j, {u'X': 4j}, {u'X': -4}),
    (-1, {u'a': 10, u'b': -20}, {u'a': -10, u'b': 20}),
))
def test_scalar_multiplication(scalar, terms, terms_expected):
    linear_dict = cirq.LinearDict(terms)
    actual_1 = scalar * linear_dict
    actual_2 = linear_dict * scalar
    expected = cirq.LinearDict(terms_expected)
    assert actual_1 == expected
    assert actual_2 == expected
    assert actual_1 == actual_2


@pytest.mark.parametrize(u'scalar, terms, terms_expected', (
    (2, {}, {}),
    (2, {u'X': 6, u'Y': -2}, {u'X': 3, u'Y': -1}),
    (1j, {u'X': 1, u'Y': 1j}, {u'X': -1j, u'Y': 1}),
    (-1, {u'a': 10, u'b': -20}, {u'a': -10, u'b': 20}),
))
def test_scalar_division(scalar, terms, terms_expected):
    linear_dict = cirq.LinearDict(terms)
    actual = linear_dict / scalar
    expected = cirq.LinearDict(terms_expected)
    assert actual == expected
    assert expected == actual


@pytest.mark.parametrize(u'expression, expected', (
    ((cirq.LinearDict({u'X': 10}) + cirq.LinearDict({u'X': 10, u'Y': -40})) / 20,
     cirq.LinearDict({u'X': 1, u'Y': -2})),
    (cirq.LinearDict({u'a': -2}) + 2 * cirq.LinearDict({u'a': 1}),
     cirq.LinearDict({})),
    (cirq.LinearDict({u'b': 2}) - 2 * cirq.LinearDict({u'b': 1}),
     cirq.LinearDict({})),
))
def test_expressions(expression, expected):
    assert expression == expected
    assert not expression != expected
    assert cirq.approx_eq(expression, expected)


@pytest.mark.parametrize(u'terms, bool_value', (
    ({}, False),
    ({u'X': 0}, False),
    ({u'Z': 1e-12}, True),
    ({u'Y': 1}, True),
))
def test_bool(terms, bool_value):
    linear_dict = cirq.LinearDict(terms)
    assert bool(linear_dict) == bool_value


@pytest.mark.parametrize(u'terms_1, terms_2', (
    ({}, {}),
    ({}, {u'X': 0}),
    ({u'X': 0.0}, {u'Y': 0.0}),
    ({u'a': 1}, {u'a': 1, u'b': 0}),
))
def test_equal(terms_1, terms_2):
    linear_dict_1 = cirq.LinearDict(terms_1)
    linear_dict_2 = cirq.LinearDict(terms_2)
    assert linear_dict_1 == linear_dict_2
    assert linear_dict_2 == linear_dict_1
    assert not linear_dict_1 != linear_dict_2
    assert not linear_dict_2 != linear_dict_1


@pytest.mark.parametrize(u'terms_1, terms_2', (
    ({}, {u'a': 1}),
    ({u'X': 1e-12}, {u'X': 0}),
    ({u'X': 0.0}, {u'Y': 0.1}),
    ({u'X': 1}, {u'X': 1, u'Z': 1e-12}),
))
def test_unequal(terms_1, terms_2):
    linear_dict_1 = cirq.LinearDict(terms_1)
    linear_dict_2 = cirq.LinearDict(terms_2)
    assert linear_dict_1 != linear_dict_2
    assert linear_dict_2 != linear_dict_1
    assert not linear_dict_1 == linear_dict_2
    assert not linear_dict_2 == linear_dict_1


@pytest.mark.parametrize(u'terms_1, terms_2', (
    ({}, {u'X': 1e-9}),
    ({u'X': 1e-12}, {u'X': 0}),
    ({u'X': 5e-10}, {u'Y': 2e-11}),
    ({u'X': 1.000000001}, {u'X': 1, u'Z': 0}),
))
def test_approximately_equal(terms_1, terms_2):
    linear_dict_1 = cirq.LinearDict(terms_1)
    linear_dict_2 = cirq.LinearDict(terms_2)
    assert cirq.approx_eq(linear_dict_1, linear_dict_2)
    assert cirq.approx_eq(linear_dict_2, linear_dict_1)


@pytest.mark.parametrize(u'a, b', (
    (cirq.LinearDict({}), None),
    (cirq.LinearDict({u'X': 0}), 0),
    (cirq.LinearDict({u'Y': 1}), 1),
    (cirq.LinearDict({u'Z': 1}), 1j),
    (cirq.LinearDict({u'I': 1}), u'I'),
))
def test_incomparable(a, b):
    assert a.__eq__(b) is NotImplemented
    assert a.__ne__(b) is NotImplemented
    assert a._approx_eq_(b, atol=1e-9) is NotImplemented


@pytest.mark.parametrize(u'terms, fmt, expected_string', (
    ({}, u'{}', u'0'),
    ({}, u'{:.2f}', u'0.00'),
    ({}, u'{:.2e}', u'0.00e+00'),
    ({u'X': 2**-10}, u'{:.2f}', u'0.00'),
    ({u'X': 1/100}, u'{:.2e}', u'1.00e-02*X'),
    ({u'X': 1j*2**-10}, u'{:.2f}', u'0.00'),
    ({u'X': 1j*2**-10}, u'{:.3f}', u'0.001j*X'),
    ({u'X': 2j, u'Y': -3}, u'{:.2f}', u'2.00j*X-3.00*Y'),
    ({u'X': -2j, u'Y': 3}, u'{:.2f}', u'-2.00j*X+3.00*Y'),
    ({u'X': np.sqrt(1j)}, u'{:.3f}', u'(0.707+0.707j)*X'),
    ({u'X': np.sqrt(-1j)}, u'{:.3f}', u'(0.707-0.707j)*X'),
    ({u'X': -np.sqrt(-1j)}, u'{:.3f}', u'(-0.707+0.707j)*X'),
    ({u'X': -np.sqrt(1j)}, u'{:.3f}', u'-(0.707+0.707j)*X'),
    ({u'X': 1, u'Y': -1, u'Z': 1j}, u'{:.5f}', u'1.00000*X-1.00000*Y+1.00000j*Z'),
    ({u'X': 2, u'Y': -0.0001}, u'{:.4f}', u'2.0000*X-0.0001*Y'),
    ({u'X': 2, u'Y': -0.0001}, u'{:.3f}', u'2.000*X'),
    ({u'X': 2, u'Y': -0.0001}, u'{:.1e}', u'2.0e+00*X-1.0e-04*Y'),
))
def test_format(terms, fmt, expected_string):
    linear_dict = cirq.LinearDict(terms)
    actual_string = fmt.format(linear_dict)
    assert actual_string.replace(u' ', u'') == expected_string.replace(u' ', u'')


@pytest.mark.parametrize(u'terms', (
    ({}, {u'X': 1}, {u'X': 2, u'Y': 3}, {u'X': 1.23456789e-12})
))
def test_repr(terms):
    original = cirq.LinearDict(terms)
    print repr(original)
    recovered = eval(repr(original))
    assert original == recovered
    assert recovered == original


@pytest.mark.parametrize(u'terms, string', (
    ({}, u'0.000'),
    ({u'X': 1.5, u'Y': 1e-5}, u'1.500*X'),
    ({u'Y': 2}, u'2.000*Y'),
    ({u'X': 1, u'Y': -1j}, u'1.000*X-1.000j*Y'),
    ({u'X': np.sqrt(3)/3, u'Y': np.sqrt(3)/3, u'Z': np.sqrt(3)/3},
     u'0.577*X+0.577*Y+0.577*Z'),
    ({u'I': np.sqrt(1j)}, u'(0.707+0.707j)*I'),
    ({u'X': np.sqrt(-1j)}, u'(0.707-0.707j)*X'),
    ({u'X': -np.sqrt(-1j)}, u'(-0.707+0.707j)*X'),
    ({u'X': -np.sqrt(1j)}, u'-(0.707+0.707j)*X'),
    ({u'X': -2, u'Y': -3}, u'-2.000*X-3.000*Y'),
    ({u'X': -2j, u'Y': -3}, u'-2.000j*X-3.000*Y'),
    ({u'X': -2j, u'Y': -3j}, u'-2.000j*X-3.000j*Y'),
))
def test_str(terms, string):
    linear_dict = cirq.LinearDict(terms)
    assert unicode(linear_dict).replace(u' ', u'') == string.replace(u' ', u'')


class FakePrinter(object):
    def __init__(self):
        self.buffer = u''

    def text(self, s):
        self.buffer += s

    def reset(self):
        self.buffer = u''


@pytest.mark.parametrize(u'terms', (
    {}, {u'Y': 2}, {u'X': 1, u'Y': -1j},
    {u'X': np.sqrt(3)/3, u'Y': np.sqrt(3)/3, u'Z': np.sqrt(3)/3},
    {u'I': np.sqrt(1j)}, {u'X': np.sqrt(-1j)},
    {cirq.X: 1, cirq.H: -1},
))
def test_repr_pretty(terms):
    printer = FakePrinter()
    linear_dict = cirq.LinearDict(terms)

    linear_dict._repr_pretty_(printer, False)
    assert printer.buffer.replace(u' ', u'') == unicode(linear_dict).replace(u' ', u'')

    printer.reset()
    linear_dict._repr_pretty_(printer, True)
    assert printer.buffer == u'LinearDict(...)'
