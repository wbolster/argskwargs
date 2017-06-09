"""
argskwargs, a flexible container for positional and keyword arguments.
"""

import functools as _functools
import itertools as _itertools

__all__ = ['argskwargs']

_yes_i_am_an_internal_call = object()


class argskwargs(object):
    """
    Container class for positional and keyword arguments.

    Instances must be treated as an immutable read-only data containers.
    """
    __slots__ = ('args', 'kwargs')

    def __init__(self, *args, **kwargs):
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

        Any positional and keyword arguments to this method will be
        merged with the arguments stored in this container.
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

        Any positional and keyword arguments to this method will be
        merged with the arguments stored in this container.
        """
        merged_kwargs = self.kwargs.copy()
        merged_kwargs.update(kwargs)
        return _functools.partial(
            callable, *(self.args + args), **merged_kwargs)

    def copy(self, *args, **kwargs):
        """
        Create a copy of this container with additional arguments.

        This is a shorthand for::

          original = argskwargs(...)
          new_instance = argskwargs(
              *original.args, *args,
              **original.kwargs, **kwargs)

        Since instances of this class are intended to be immutable, this
        method is useful to create a new container instance with
        additional arguments.

        Any positional and keyword arguments to this method will be
        merged with the arguments stored in this container.
        """
        if not args and not kwargs:
            return self
        return self.apply(argskwargs, *args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.args, self.kwargs) == (other.args, other.kwargs)
        return NotImplemented

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
