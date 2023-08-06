# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Base class for plum type metaclasses."""


class PlumType(type):

    """Base class for plum types."""

    __nbytes__ = -1

    def __view__(cls, plumtype, memory, offset=0):
        """Create plum view of memory bytes.

        :param PlumType datatype: datatype to view
        :param MemoryInterface memory: memory bytes
        :param int offset: byte offset

        """
        raise TypeError(f'{cls.__name__!r} does not support view()')
