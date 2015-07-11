"""
argskwargs, a flexible container for positional and keyword arguments.
"""

import functools as _functools
import itertools as _itertools

__all__ = ['argskwargs']


class _ArgsKwargs(object):
    """
    Container class for positional and keyword arguments.

    While not enforced, instances must be treated as immutable read-only
    data containers.

    Do not instantiate directly; use the argskwargs() function instead.
    """

    __slots__ = ('args', 'kwargs')

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        chunks = _itertools.chain(
            # Positional arguments
            (repr(arg) for arg in self.args),

            # Keyword arguments
            ('{0}={1!r}'.format(name, value)
             for name, value in sorted(self.kwargs.items()))
        )
        return 'argskwargs({0})'.format(', '.join(chunks))

    def __str__(self):
        return repr(self)

    def __iter__(self):
        yield self.args
        yield self.kwargs

    def apply(self, callable, *args, **kwargs):
        """
        Invoke the specified callable with the stored arguments.

        Any additional positional and keyword arguments will be merged
        with the arguments stored on this instance.
        """

        # No additional arguments specifed; avoid copying.
        if not args and not kwargs:
            return callable(*self.args, **self.kwargs)

        # Combine stored arguments with method arguments.
        merged_kwargs = self.kwargs.copy()
        merged_kwargs.update(kwargs)
        return callable(*(self.args + args), **merged_kwargs)

    __call__ = apply

    def partial(self, callable, *args, **kwargs):
        """
        Return a `partial` function with the stored arguments.

        See `functools.partial` in the standard library for details
        about partial functions.

        Any additional positional and keyword arguments will be merged
        with the arguments stored on this instance.
        """
        merged_kwargs = self.kwargs.copy()
        merged_kwargs.update(kwargs)
        return _functools.partial(
            callable, *(self.args + args), **merged_kwargs)

    def copy(self, *args, **kwargs):
        if not args and not kwargs:
            return self
        return self.apply(argskwargs, *args, **kwargs)

    def __eq__(self, other):
        if type(other) is not _ArgsKwargs:
            return False
        return (self.args, self.kwargs) == (other.args, other.kwargs)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __getstate__(self):
        return self.args, self.kwargs

    def __setstate__(self, state):
        self.args, self.kwargs = state


def argskwargs(*args, **kwargs):
    """
    Return a new argskwargs() instance that holds the passed arguments.

    The return instance must be treated as an immutable read-only object.
    """
    return _ArgsKwargs(args, kwargs)
