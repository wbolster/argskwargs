import copy
import pickle

from argskwargs import argskwargs


def test_named_access():
    """Instances have args and kwargs attributes."""
    ak = argskwargs(1, 2, a=3, b=[4, 5])
    assert ak.args == (1, 2)
    assert ak.kwargs == dict(a=3, b=[4, 5])


def test_unpacking():
    """Instances can be unpacked into an (args, kwargs) tuple."""
    ak = argskwargs(1, 2, a=3, b=[4, 5])
    actual_args, actual_kwargs = ak
    assert actual_args == (1, 2)
    assert actual_kwargs == dict(a=3, b=[4, 5])


def test_repr():
    """The repr() returns valid code (depends on repr() on args)."""
    actual = repr(argskwargs())
    expected = 'argskwargs()'
    assert actual == expected

    ak = argskwargs(1, 2, a=3, b=[4, 5])
    actual = repr(ak)
    expected = 'argskwargs(1, 2, a=3, b=[4, 5])'
    assert actual == expected


def test_str():
    """The string representation is the same as the repr()."""
    ak = argskwargs(1, 2, a=3, b=[4, 5])
    assert str(ak) == repr(ak)


def test_copy():
    """The copy() method can be used to extend the object."""
    ak = argskwargs(1, a='aa', b='foo').copy(2, b='bb')
    assert ak.args == (1, 2)
    assert ak.kwargs == dict(a='aa', b='bb')
    assert ak == ak.copy()


def returner(*args, **kwargs):
    """Test helper simply returns any args and kwargs."""
    return args, kwargs


def test_apply():
    """The apply() method passes args and kwargs along."""
    ak = argskwargs(1, a='aa')
    actual = ak.apply(returner)
    expected = (1,), {'a': 'aa'}
    assert actual == expected


def test_apply_extra_args():
    """The apply() method merges additional args and kwargs."""
    ak = argskwargs(1, a='aa', b='will-be-overridden')
    actual = ak.apply(returner, 2, b='bb')
    expected = (1, 2), {'a': 'aa', 'b': 'bb'}
    assert actual == expected


def test_callable():
    """Instances are callable as a shortcut to .apply()."""
    ak = argskwargs(1, a='aa')
    actual = ak(returner)
    expected = (1,), {'a': 'aa'}
    assert actual == expected


def test_partial():
    """The partial() method returns a partial function."""
    ak = argskwargs(1, a='aa')
    f = ak.partial(returner)
    actual = f()
    expected = (1,), {'a': 'aa'}
    assert actual == expected


def test_partial_extra_args():
    """The partial() method merges additional args and kwargs."""
    ak = argskwargs(1, a='aa', b='will-be-overridden')
    f = ak.partial(returner, 2, b='bb')

    actual = f()
    expected = (1, 2), {'a': 'aa', 'b': 'bb'}
    assert actual == expected

    actual = f(3, c='cc')
    expected = (1, 2, 3), {'a': 'aa', 'b': 'bb', 'c': 'cc'}
    assert actual == expected


def test_equality():
    """Instances can be compared for (in)equality."""
    a = argskwargs(1, a='aa')
    b = argskwargs(1, a='aa')
    assert a == b
    assert not (a != b)
    c = argskwargs(2)
    assert not (a == c)
    assert a != c
    assert a != object()


def test_instance_copying():
    """Instances are (intended to be) immutable, hence copying is cheap."""
    ak = argskwargs(1, a='aa')
    ak2 = copy.copy(ak)
    assert ak is ak2
    ak3 = copy.deepcopy(ak)
    assert ak is ak3


def test_pickle():
    """Instances can be (un)pickled."""
    ak = argskwargs(1, a='aa')
    ak2 = pickle.loads(pickle.dumps(ak))
    assert ak2.args == (1,)
    assert ak2.kwargs == {'a': 'aa'}
