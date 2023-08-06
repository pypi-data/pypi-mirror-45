# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Plum view base class."""

from math import ceil, floor

from plum._plumtype import PlumType
from plum.memory._base_interface import MemoryInterface


class PlumView:

    """Plum view base class.

    :param PlumType plumtype: associated plum type
    :param MemoryInterface memory: memory bytes
    :param int offset: byte offset

    """

    def __init__(self, plumtype, memory, offset):
        if not isinstance(plumtype, PlumType):
            raise TypeError("target must be a PlumType class")

        if not isinstance(memory, MemoryInterface):
            raise TypeError("source bytes must be a memory interface instance")

        if offset < 0:
            raise ValueError("byte offset must be greater than or equal to zero")

        self.__type__ = plumtype
        self.__memory__ = memory
        self.__offset__ = offset

    def __getvalue__(self):
        """Unpack value from underlying memory.

        :returns: plum instance
        :rtype: cls

        """
        raise NotImplementedError(  # pragma: no cover
            f"{self.__class__.__name__!r} does not support getvalue()")

    def __setvalue__(self, value):
        """Pack value into underlying memory.

        :param object value: new value

        """
        raise NotImplementedError(  # pragma: no cover
            f"{self.__class__.__name__!r} does not support setvalue()")


class NumberView(PlumView):

    """Numeric view class."""

    def __abs__(self):
        return abs(self.__getvalue__())

    def __add__(self, other):
        return self.__getvalue__() + other

    def __divmod__(self, other):
        return divmod(self.__getvalue__(), other)

    def __float__(self):
        return float(self.__getvalue__())

    def __ge__(self, other):
        return self.__getvalue__() >= other

    def __getvalue__(self):
        """Unpack value from underlying memory.

        :returns: plum instance
        :rtype: cls

        """
        # include copy here to avoid pylint unimplemented method warning
        raise NotImplementedError(  # pragma: no cover
            f"{self.__class__.__name__!r} does not support getvalue()")

    def __gt__(self, other):
        return self.__getvalue__() > other

    def __iadd__(self, other):
        self.__setvalue__(self.__getvalue__() + other)
        return self

    def __imod__(self, other):
        self.__setvalue__(self.__getvalue__() % other)
        return self

    def __imul__(self, other):
        self.__setvalue__(self.__getvalue__() * other)
        return self

    def __int__(self):
        return int(self.__getvalue__())

    def __ipow__(self, other):
        self.__setvalue__(self.__getvalue__() ** other)
        return self

    def __isub__(self, other):
        self.__setvalue__(self.__getvalue__() - other)
        return self

    def __le__(self, other):
        return self.__getvalue__() <= other

    def __lt__(self, other):
        return self.__getvalue__() < other

    def __mod__(self, other):
        return self.__getvalue__() % other

    def __mul__(self, other):
        return self.__getvalue__() * other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __neg__(self):
        return -self.__getvalue__()

    def __pos__(self):
        return +self.__getvalue__()

    def __pow__(self, exponent):
        return self.__getvalue__().__pow__(exponent)

    def __radd__(self, other):
        return other + self.__getvalue__()

    def __rdivmod__(self, other):
        return divmod(other, self.__getvalue__())

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__getvalue__()})"

    def __rmod__(self, other):
        return other % self.__getvalue__()

    def __rmul__(self, other):
        return other * self.__getvalue__()

    def __rpow__(self, other):
        return other ** self.__getvalue__()

    def __rsub__(self, other):
        return other - self.__getvalue__()

    def __rtruediv__(self, other):
        return other / self.__getvalue__()

    def __setvalue__(self, value):
        """Pack value into underlying memory.

        :param object value: new value

        """
        # include copy here to avoid pylint unimplemented method warning
        raise NotImplementedError(  # pragma: no cover
            f"{self.__class__.__name__!r} does not support setvalue()")

    def __str__(self):
        return str(self.__getvalue__())

    def __sub__(self, other):
        return self.__getvalue__() - other

    def __truediv__(self, other):
        return self.__getvalue__() / other

    def __ceil__(self):
        return ceil(self.__getvalue__())

    def __floor__(self):
        return floor(self.__getvalue__())

    def __floordiv__(self, other):
        return self.__getvalue__().__floordiv__(other)

    def __rfloordiv__(self, other):
        return self.__getvalue__().__rfloordiv__(other)

    def __round__(self, ndigits=None):
        return self.__getvalue__().__round__(ndigits)

    def __trunc__(self):
        return self.__getvalue__().__trunc__()
