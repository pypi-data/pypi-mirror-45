# -*- coding: utf-8 -*-

from collections import namedtuple


Value = namedtuple('value', ['value'])

Property = namedtuple('prop', ['path'])

SortProperty = namedtuple('sortprop', ['prefix', 'path'])

Sort = namedtuple('sort', ['sortprops'])

Select = namedtuple('select', ['props'])

Values = namedtuple('values', ['prop'])

Distinct = namedtuple('distinct', [])

Aggregate = namedtuple('aggregate', ['props'])

In = namedtuple('in_', ['prop', 'values'])

Out = namedtuple('out', ['prop', 'values'])

Contains = namedtuple('contains', ['prop', 'expr'])

Excludes = namedtuple('excludes', ['prop', 'expr'])

Limit = namedtuple('limit', ['count', 'start', 'max_count'])

And = namedtuple('and_', ['queries'])

Or = namedtuple('or_', ['queries'])

Eq = namedtuple('eq', ['prop', 'expr'])

Lt = namedtuple('lt', ['prop', 'expr'])

Le = namedtuple('le', ['prop', 'expr'])

Gt = namedtuple('gt', ['prop', 'expr'])

Ge = namedtuple('ge', ['prop', 'expr'])

Ne = namedtuple('ne', ['prop', 'expr'])

#Rel

Sum = namedtuple('sum_', ['prop'])

Mean = namedtuple('mean', ['prop'])

Max = namedtuple('max_', ['prop'])

Min = namedtuple('min_', ['prop'])

Recurse = namedtuple('recurse', ['prop'])

First = namedtuple('first', [])

One = namedtuple('one', [])

Count = namedtuple('count', [])
