# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Integer type."""

from ._inttype import IntType
from ._intview import IntView
from .._plum import Plum
from .._utils import getbytes


class Int(int, Plum, metaclass=IntType):

    """Interpret memory bytes as an integer.

    :param x: value
    :type x: number or str
    :param int base: base of x when x is ``str``

    """

    _byteorder = 'little'
    __max__ = 0xffffffff
    _min = 0
    __nbytes__ = 4
    _signed = False

    __equivalent__ = int

    @classmethod
    def _add_flags_to_dump(cls, value, dump):
        pass

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent):
        chunk, offset, limit = getbytes(
            memory, offset, cls.__nbytes__, limit, dump, cls)

        self = int.from_bytes(chunk, cls._byteorder, signed=cls._signed)

        if dump:
            dump.value = self
            cls._add_flags_to_dump(self, dump)

        return self, offset, limit

    @classmethod
    def __pack__(cls, memory, offset, value, dump):
        nbytes = cls.__nbytes__

        if dump:
            dump.cls = cls

        try:
            to_bytes = value.to_bytes
        except AttributeError:
            raise TypeError(f'value must be int or int-like')

        chunk = to_bytes(nbytes, cls._byteorder, signed=cls._signed)

        if dump:
            dump.value = value
            dump.memory = chunk
            cls._add_flags_to_dump(value, dump)

        end = offset + nbytes
        memory[offset:end] = chunk

        return end

    def __str__(self):
        return int.__str__(self)

    def __baserepr__(self):
        return int.__repr__(self)

    __repr__ = Plum.__repr__

    @staticmethod
    def __view__(plumtype, memory, offset=0):
        return IntView(plumtype, memory, offset)
