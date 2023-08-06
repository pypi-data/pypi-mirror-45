# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Integer type view."""

from numbers import Integral

from plum import pack, unpack
from plum._plumview import NumberView


class IntView(NumberView, Integral):  # pylint: disable=too-many-ancestors

    """Integer type view."""

    def __and__(self, other):
        return self.__getvalue__() & other

    def __eq__(self, other):
        return self.__getvalue__() == other

    def __getvalue__(self):
        """Unpack float from underlying memory."""
        return unpack(self.__type__, self.__memory__.get_bytes(
            self.__type__.__nbytes__, offset=self.__offset__))

    def __iand__(self, other):
        self.__setvalue__(self.__getvalue__() & other)
        return self

    def __ilshift__(self, other):
        self.__setvalue__(self.__getvalue__() << other)
        return self

    __int__ = __getvalue__

    def __invert__(self):
        return ~self.__getvalue__()

    def __ior__(self, other):
        self.__setvalue__(self.__getvalue__() | other)
        return self

    def __irshift__(self, other):
        self.__setvalue__(self.__getvalue__() >> other)
        return self

    def __ixor__(self, other):
        self.__setvalue__(self.__getvalue__() ^ other)
        return self

    def __lshift__(self, other):
        return self.__getvalue__() << other

    def __or__(self, other):
        return self.__getvalue__() | other

    def __rand__(self, other):
        return other & self.__getvalue__()

    def __rlshift__(self, other):
        return other << self.__getvalue__()

    def __ror__(self, other):
        return other | self.__getvalue__()

    def __rrshift__(self, other):
        return other >> self.__getvalue__()

    def __rshift__(self, other):
        return self.__getvalue__() >> other

    def __rxor__(self, other):
        return other ^ self.__getvalue__()

    def __setvalue__(self, value):
        """Pack value into underlying memory.

        :param object value: new value

        """
        self.__memory__.set_bytes(pack(self.__type__, value), offset=self.__offset__)

    def __xor__(self, other):
        return self.__getvalue__() ^ other

    def to_bytes(self, length, byteorder, *, signed=False):
        """Return an array of bytes representing an integer.

        :param int length:
            Length of bytes object to use.  An OverflowError is raised if the
            integer is not representable with the given number of bytes.

        :param str byteorder:
            The byte order used to represent the integer.  If byteorder is 'big',
            the most significant byte is at the beginning of the byte array.  If
            byteorder is 'little', the most significant byte is at the end of the
            byte array.  To request the native byte order of the host system, use
            ``sys.byteorder`` as the byte order value.

        :param bool signed:
            Determines whether two's complement is used to represent the integer.
            If signed is False and a negative integer is given, an OverflowError
            is raised.

        :returns: array of bytes
        :rtype: bytes

        """
        return self.__getvalue__().to_bytes(length, byteorder, signed=signed)
