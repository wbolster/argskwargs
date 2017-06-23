==========
argskwargs
==========

.. py:currentmodule:: argskwargs

:py:class:`argskwargs` is a small Python library that provides a
flexible container for positional and keyword arguments.

Passing around arguments for a function
without actually calling that function (at least not yet)
typically involves two variables
that are closely kept together:

* a tuple, often called ``args``
* a dict, often called ``kwargs``

This library simplifies this clunky and error-prone code pattern
by putting these two values inside a small container,
named :py:class:`argskwargs`.


Installation
============

::

  pip install argskwargs

:py:class:`argskwargs` can be used on Python 3.3+ and Python 2.6+.

Usage
=====

An :py:class:`argskwargs` container stores arbitrary
positional arguments (:py:attr:`~argskwargs.args`)
and keyword arguments (:py:attr:`~argskwargs.kwargs`).
This container is essentially the same
as a ``(args, kwargs)`` tuple,
but with a nice and small API on top
to keep your code simple and clear.

To get started, import :py:class:`argskwargs`::

  >>> from argskwargs import argskwargs

To make a container,
pass arbitrary positional and keyword arguments
to the :py:class:`argskwargs` class constructor::

  >>> my_args = argskwargs(1, 2, foo='bar')
  >>> my_args
  argskwargs(1, 2, foo='bar')

To obtain a tuple and a dict, unpack the container::

  >>> x, y = my_args
  >>> x
  (1, 2)
  >>> y
  {'foo': 'bar'}

Alternatively, access the :py:attr:`~argskwargs.args` and
:py:attr:`~argskwargs.kwargs` attributes::

  >>> my_args.args
  (1, 2)
  >>> my_args.kwargs
  {'foo': 'bar'}


Calling functions
-----------------

Here is a function that simply prints out
anything that is passed to it::

  >>> import pprint
  >>> def print_arguments(*args, **kwargs):
  ...     print('positional arguments ' + str(args))
  ...     print('keyword arguments ' + pprint.pformat(kwargs))

(Note: dictionary order cannot be relied on in most Python versions.
The use of ``pformat()`` makes the output deterministic,
since that function will sort the dict keys.
All the sample code in this documentation
is actually executed as part of the tests for this library,
and deterministic output is required
for those doctests to pass successfully.)

This function can be called directly using ‘splat’ syntax::

  >>> print_arguments(*my_args.args, **my_args.kwargs)
  positional arguments (1, 2)
  keyword arguments {'foo': 'bar'}

Arguably, this is not much better than
using using two variables
for the positional and keyword arguments,
so let's see what makes :py:class:`argskwargs` useful.
Here is another way to do the same
using the :py:meth:`~argskwargs.apply()` method:

  >>> my_args.apply(print_arguments)
  positional arguments (1, 2)
  keyword arguments {'foo': 'bar'}

Since this is the typical use case for :py:class:`argskwargs`,
you can also omit :py:meth:`~argskwargs.apply()`
and call the instance directly::

  >>> my_args(print_arguments)
  positional arguments (1, 2)
  keyword arguments {'foo': 'bar'}

As you can see the code is inverted:
the callable is passed to the arguments,
instead of the other way around,
as would be the case for a normal function call.

Now, assume that you want to pass
more arguments to ``print_arguments()``
than those stored in the :py:class:`argskwargs` instance.
Just pass them in::

  >>> my_args(print_arguments, 3, 4, abc='xyz')
  positional arguments (1, 2, 3, 4)
  keyword arguments {'foo': 'bar', 'abc': 'xyz'}

The additional positional arguments extend
the existing positional arguments,
and the additional keyword arguments augment (or override)
the existing keyword arguments.


Making copies with additional arguments
---------------------------------------

To extend an :py:class:`argskwargs` instance,
use the :py:meth:`~argskwargs.copy()` method,
which does exactly that::

  >>> more_args = my_args.copy(3, 4, abc='xyz')
  >>> more_args
  argskwargs(1, 2, 3, 4, abc='xyz', foo='bar')

This new argument container can now be used like the original one:

  >>> more_args(print_arguments)
  positional arguments (1, 2, 3, 4)
  keyword arguments {'abc': 'xyz', 'foo': 'bar'}


Using partial functions
-----------------------

In a sense, :py:class:`argskwargs` is the missing companion to
``functools.partial()`` from the Python standard library.
A partial function (or ‘partial object’)
can also hold positional and keyword arguments,
but cannot be used without a callable.

To create a partial function
from a :py:class:`argskwargs` container,
use the :py:meth:`~argskwargs.partial()` method
and provide it with a callable::

  >>> f = my_args.partial(print_arguments)

The resulting partial function can be called as usual::

  >>> f()
  positional arguments (1, 2)
  keyword arguments {'foo': 'bar'}

Partial functions allow additional arguments::

  >>> f(3, 4, abc='xyz')
  positional arguments (1, 2, 3, 4)
  keyword arguments {'abc': 'xyz', 'foo': 'bar'}

For completeness, you can pass more arguments
when creating the partial function,
and even more when calling it::

  >>> g = my_args.partial(print_arguments, 3, 4, foo='foofoo')
  >>> g(5, 6, bar='baz')
  positional arguments (1, 2, 3, 4, 5, 6)
  keyword arguments {'bar': 'baz', 'foo': 'foofoo'}

You may want to avoid these more complex forms,
since those will likely not improve code clarity.
Or as the Python mantras go:
*readability counts* and *simple is better than complex*.


API
===

.. autoclass:: argskwargs
   :members:
   :special-members:
   :member-order: bysource


Contributing
============

The source code and issue tracker for this package can be found on Github:

  https://github.com/wbolster/argskwargs


License
=======

*(This is the OSI approved 3-clause "New BSD License".)*

Copyright © 2015–2017, Wouter Bolsterlee

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

* Neither the name of the author nor the names of its contributors may be used
  to endorse or promote products derived from this software without specific
  prior written permission.

This software is provided by the copyright holders and contributors "as is" and
any express or implied warranties, including, but not limited to, the implied
warranties of merchantability and fitness for a particular purpose are
disclaimed. In no event shall the copyright holder or contributors be liable
for any direct, indirect, incidental, special, exemplary, or consequential
damages (including, but not limited to, procurement of substitute goods or
services; loss of use, data, or profits; or business interruption) however
caused and on any theory of liability, whether in contract, strict liability,
or tort (including negligence or otherwise) arising in any way out of the use
of this software, even if advised of the possibility of such damage.
