# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Local shared memory interface."""

from plum._exceptions import ExcessMemoryError, InsufficientMemoryError
from plum.memory._base_interface import MemoryInterface


class LocalMemory(MemoryInterface):

    """Local shared memory interface.

    :param data: memory bytes
    :type data: bytearray, memoryview, or bytes

    """

    def __init__(self, data):
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise ValueError("expected a bytes, bytearray, or memoryview instance")

        self._data = data

    def get_bytes(self, nbytes, offset=0):
        """Get local memory bytes.

        :param int nbytes: number of bytes to get
        :param int offset: byte offset
        :returns: memory byte(s)
        :rtype: bytearray

        """
        if nbytes <= 0:
            raise ValueError("number of bytes must be a positive integer")

        if offset < 0:
            raise ValueError("offset must be greater than or equal to zero")

        retval = self._data[offset:offset + nbytes]

        if nbytes != len(retval):
            raise InsufficientMemoryError("not enough memory bytes to get")

        return retval

    def set_bytes(self, data, offset=0):
        """Set local memory bytes.

        :param bytearray data: new bytes
        :param int offset: byte offset

        """
        if offset < 0:
            raise ValueError("offset must be greater than or equal to zero")

        if offset >= len(self._data):
            raise ValueError("offset exceeds memory bytes")

        if len(data) + offset > len(self._data):
            extra_bytes = data[len(self._data) - len(data) - offset:]
            raise ExcessMemoryError("too many memory bytes to set", extra_bytes)

        self._data[offset:offset + len(data)] = data

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self._data)})"
