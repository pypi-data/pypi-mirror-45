# Bsearch

[![Build Status](https://travis-ci.org/domsleee/bsearch.svg?branch=master)](https://travis-ci.org/domsleee/bsearch)
[![PyPI shield](https://img.shields.io/pypi/v/bsearch.svg?style=flat-square)](https://pypi.org/project/bsearch/)

Binary search in python with more flexible comparisons.

## Installation

~~~bash
pip install bsearch
~~~

## Usage

`bisect_left` and `bisect_right` are backwards compatible with the [bisect](https://docs.python.org/3/library/bisect.html) library. For example:

~~~python
from bsearch import bisect_left
a = [1,2,3,4,5]
i = bisect_left(a, 4) # returns 3
~~~

You can use the `key` option to search arrays of different types

~~~python
from bsearch import bisect_left
a = [(1,100), (2, 100), (5,200)]

# using the first element of the tuple as the key
i = bisect_left(a, 2, key=lambda x: x[0]) # returns 1
~~~

To search descending list, use the wrapper `binary_search`, and provide an operator. This will return the smallest  `i` such that `op(a[i], v)`

~~~python
from bsearch import binary_search
a = [5, 4, 3, 2]
i = binary_search(a, 4, op=lambda a b: a >= b) # returns 1
~~~