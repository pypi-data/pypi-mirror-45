# post-tonal-theory-helper

#### by Mari Masuda <mbmasuda.github@gmail.com>

This package provides some basic post-tonal music theory
analysis functions for Python 3.

Based on the text *Introduction to Post-Tonal Theory*
by Joseph N. Straus (ISBN 0-13-686692-1)


## Installation

```bash
$ pip install post-tonal-theory-helper-mbmasuda
```

## Usage

```python
from ptth.api import *

pitches = '0t38e'

normal = normal_form(pitches)
prime = prime_form(pitches)

normal_t4 = transpose(normal, 4)
normal_t4i = invert(normal, transpose=4)

boolean1 = is_transpositionally_related(normal, prime)
boolean2 = is_inversionally_related(normal, prime)

members = get_set_class_members(normal)
```

## Tests

Tests can be run with pytest