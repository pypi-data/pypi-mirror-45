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

u"""Linear combination represented as mapping of things to coefficients."""

from __future__ import division
from __future__ import absolute_import
from typing import (Any, Callable, Dict, ItemsView, Iterable, Iterator,
                    KeysView, Mapping, MutableMapping, overload, Tuple, TypeVar,
                    Union, ValuesView)

Scalar = Union[complex, float]
TVector = TypeVar(u'TVector')

TDefault = TypeVar(u'TDefault')


class LinearDict(MutableMapping[TVector, Scalar]):
    u"""Represents linear combination of things.

    LinearDict implements the basic linear algebraic operations of vector
    addition and scalar multiplication for linear combinations of abstract
    vectors. Keys represent the vectors, values represent their coefficients.
    The only requirement on the keys is that they be hashable (i.e. are
    immutable and implement __hash__ and __eq__ with equal objects hashing
    to equal values).

    A consequence of treating keys as opaque is that all relationships between
    the keys other than equality are ignored. In particular, keys are allowed
    to be linearly dependent.
    """
    def __init__(self,
                 terms,
                 validator=lambda _: True):
        u"""Initializes linear combination from a collection of terms.

        Args:
            terms: Mapping of abstract vectors to coefficients in the linear
                combination being initialized.
            validator: Optional predicate that determines whether a vector is
                valid or not. Dictionary and linear algebra operations that
                would lead to the inclusion of an invalid vector into the
                combination raise ValueError exception. By default all vectors
                are valid.
        """
        self._is_valid = validator
        self._terms = dict()  # type: Dict[TVector, Scalar]
        self.update(terms)

    TSelf = TypeVar(u'TSelf', bound=u'LinearDict[TVector]')

    @classmethod
    def fromkeys(cls, vectors, coefficient=0):
        return LinearDict(dict.fromkeys(vectors, complex(coefficient)))

    def _check_vector_valid(self, vector):
        if not self._is_valid(vector):
            raise ValueError(
                    u'{} is not compatible with linear combination {}'
                    .format(vector, self))

    def clean(self, **_3to2kwargs):
        if 'atol' in _3to2kwargs: atol = _3to2kwargs['atol']; del _3to2kwargs['atol']
        else: atol = 1e-9
        u"""Remove terms with coefficients of absolute value atol or less."""
        negligible = [v for v, c in self._terms.items() if abs(c) <= atol]
        for v in negligible:
            del self._terms[v]
        return self

    def copy(self):
        factory = type(self)
        return factory(self._terms.copy())

    def keys(self):
        snapshot = self.copy().clean(atol=0)
        return snapshot._terms.keys()

    def values(self):
        snapshot = self.copy().clean(atol=0)
        return snapshot._terms.values()

    def items(self):
        snapshot = self.copy().clean(atol=0)
        return snapshot._terms.items()

    # pylint: disable=function-redefined
    @overload
    def update(self, other, **kwargs):
        pass

    @overload
    def update(self,
               other,
               **kwargs):
        pass

    @overload
    def update(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        terms = dict()
        terms.update(*args, **kwargs)
        for vector, coefficient in terms.items():
            self[vector] = coefficient
        self.clean(atol=0)

    @overload
    def get(self, vector):
        pass

    @overload
    def get(self, vector, default
            ):
        pass

    def get(self, vector, default=0):
        if self._terms.get(vector, 0) == 0:
            return default
        return self._terms.get(vector)
    # pylint: enable=function-redefined

    def __contains__(self, vector):
        return vector in self._terms and self._terms[vector] != 0

    def __getitem__(self, vector):
        return self._terms.get(vector, 0)

    def __setitem__(self, vector, coefficient):
        self._check_vector_valid(vector)
        if coefficient != 0:
            self._terms[vector] = coefficient
            return
        if vector in self._terms:
            del self._terms[vector]

    def __delitem__(self, vector):
        if vector in self._terms:
            del self._terms[vector]

    def __iter__(self):
        snapshot = self.copy().clean(atol=0)
        return snapshot._terms.__iter__()

    def __len__(self):
        return len([v for v, c in self._terms.items() if c != 0])

    def __iadd__(self, other):
        for vector, other_coefficient in other.items():
            old_coefficient = self._terms.get(vector, 0)
            new_coefficient = old_coefficient + other_coefficient
            self[vector] = new_coefficient
        return self.clean(atol=0)

    def __add__(self, other):
        result = self.copy()
        result += other
        return result

    def __isub__(self, other):
        for vector, other_coefficient in other.items():
            old_coefficient = self._terms.get(vector, 0)
            new_coefficient = old_coefficient - other_coefficient
            self[vector] = new_coefficient
        self.clean(atol=0)
        return self

    def __sub__(self, other):
        result = self.copy()
        result -= other
        return result

    def __neg__(self):
        factory = type(self)
        return factory(dict((v, -c) for v, c in self.items()))

    def __imul__(self, a):
        for vector in self:
            self._terms[vector] *= a
        self.clean(atol=0)
        return self

    def __mul__(self, a):
        result = self.copy()
        result *= a
        return result

    def __rmul__(self, a):
        return self.__mul__(a)

    def __truediv__(self, a):
        return self.__mul__(1 / a)

    def __nonzero__(self):
        return not all(c == 0 for c in self._terms.values())

    def __eq__(self, other):
        u"""Checks whether two linear combinations are exactly equal.

        Presence or absence of terms with coefficients exactly equal to
        zero does not affect outcome.

        Not appropriate for most practical purposes due to sensitivity to
        numerical error in floating point coefficients. Use cirq.approx_eq()
        instead.
        """
        if not isinstance(other, LinearDict):
            return NotImplemented

        all_vs = set(self.keys()) | set(other.keys())
        return all(self[v] == other[v] for v in all_vs)

    def __ne__(self, other):
        u"""Checks whether two linear combinations are not exactly equal.

        See __eq__().
        """
        if not isinstance(other, LinearDict):
            return NotImplemented

        return not self == other

    def _approx_eq_(self, other, atol):
        u"""Checks whether two linear combinations are approximately equal."""
        if not isinstance(other, LinearDict):
            return NotImplemented

        all_vs = set(self.keys()) | set(other.keys())
        return all(abs(self[v] - other[v]) < atol for v in all_vs)

    @staticmethod
    def _format_coefficient(format_spec, coefficient):
        coefficient = complex(coefficient)
        real_str = u'{:{fmt}}'.format(coefficient.real, fmt=format_spec)
        imag_str = u'{:{fmt}}'.format(coefficient.imag, fmt=format_spec)
        if float(real_str) == 0 and float(imag_str) == 0:
            return u''
        if float(imag_str) == 0:
            return real_str
        if float(real_str) == 0:
            return imag_str + u'j'
        if real_str[0] == u'-' and imag_str[0] == u'-':
            return u'-({}+{}j)'.format(real_str[1:], imag_str[1:])
        if imag_str[0] in [u'+', u'-']:
            return u'({}{}j)'.format(real_str, imag_str)
        return u'({}+{}j)'.format(real_str, imag_str)

    @staticmethod
    def _format_term(format_spec,
                     vector,
                     coefficient):
        coefficient_str = LinearDict._format_coefficient(
                format_spec, coefficient)
        if not coefficient_str:
            return coefficient_str
        result = u'{}*{!s}'.format(coefficient_str, vector)
        if result[0] in [u'+', u'-']:
            return result
        return u'+' + result

    def __format__(self, format_spec):
        formatted_terms = [self._format_term(format_spec, v, self[v])
                           for v in sorted(self.keys(), key=unicode)]
        s = u''.join(formatted_terms)
        if not s:
            return u'{:{fmt}}'.format(0, fmt=format_spec)
        if s[0] == u'+':
            return s[1:]
        return s

    def __repr__(self):
        coefficients = dict(self)
        class_name = self.__class__.__name__
        return u'cirq.{}({!r})'.format(class_name, coefficients)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.__format__(u'.3f')

    def _repr_pretty_(self, p, cycle):
        if cycle:
            class_name = self.__class__.__name__
            p.text(u'{}(...)'.format(class_name))
        else:
            p.text(unicode(self))
