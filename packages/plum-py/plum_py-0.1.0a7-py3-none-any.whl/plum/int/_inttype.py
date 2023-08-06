# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Integer type metaclass."""

from .. import boost
from .._plumtype import PlumType


class IntType(PlumType):

    """Int type metaclass.

    Create custom |Int| subclass. For example:

        >>> from plum.int import Int
        >>> class SInt24(Int, nbytes=3, signed=True, byteorder='big'):
        ...     pass
        ...
        >>>

    :param int nbytes: number of memory bytes
    :param bool signed: signed integer
    :param str byteorder: ``'big'`` or ``'little'``

    """

    __unpack_int__ = True

    def __new__(mcs, name, bases, namespace, nbytes=None, signed=None, byteorder=None):
        # pylint: disable=too-many-arguments, unused-argument
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace, nbytes=None, signed=None, byteorder=None):
        # pylint: disable=too-many-arguments
        super().__init__(name, bases, namespace)

        if nbytes is None:
            nbytes = cls.__nbytes__

        nbytes = int(nbytes)

        assert nbytes > 0

        if signed is None:
            signed = cls._signed

        signed = bool(signed)

        if byteorder is None:
            byteorder = cls._byteorder

        assert byteorder in {'big', 'little'}

        if signed:
            minvalue = -(1 << (nbytes * 8 - 1))
            maxvalue = (1 << (nbytes * 8 - 1)) - 1
        else:
            minvalue = 0
            maxvalue = (1 << (nbytes * 8)) - 1

        cls._byteorder = byteorder
        cls.__max__ = maxvalue
        cls._min = minvalue
        cls.__nbytes__ = nbytes
        cls._signed = signed

        if boost:
            cls.__unpack_fast__ = boost.fastint.add_c_acceleration(
                cls, nbytes, byteorder == 'little', signed, type(cls).__unpack_int__)
