# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Interpret memory bytes as integer enumerated constants."""

import enum

from ..._utils import getbytes
from .._int import Int
from ._enumtype import EnumType


class Enum(Int, enum.Enum, metaclass=EnumType):

    """Interpret memory bytes as integer enumerated constants.

    :param x: value
    :type x: number or str
    :param int base: base of x when x is ``str``

    """

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent):
        chunk, offset, limit = getbytes(
            memory, offset, cls.__nbytes__, limit, dump, cls)

        self = cls.from_bytes(chunk, cls._byteorder, signed=cls._signed)

        if dump:
            dump.value = self
            cls._add_flags_to_dump(self, dump)

        return self, offset, limit

    __str__ = enum.IntEnum.__str__

    def __repr__(self):
        # override so representation turns out in Python 3.6
        # e.g. <Sample.A: Int(1)> -> <Sample.A: 1>
        enum_repr = enum.IntEnum.__repr__(self)
        if '(' in enum_repr:  # pragma: no cover
            beg, _, int_repr, _ = enum_repr.replace('(', ' ').replace(')', ' ').split()
            enum_repr = f'{beg} {int_repr}>'
        return enum_repr
