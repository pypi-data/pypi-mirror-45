# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Memory interface abstract base class."""


class MemoryInterface:

    """Memory interface abstract base class."""

    def get_bytes(self, nbytes, offset=0):
        """Get memory bytes.

        :param int nbytes: number of bytes to get
        :param int offset: byte offset
        :returns: memory byte(s)
        :rtype: bytearray

        """
        raise NotImplementedError(f'{self.__class__.__name__!r} does not support get_bytes method')

    def set_bytes(self, data, offset=0):
        """Set memory bytes.

        :param bytearray data: new bytes
        :param int offset: byte offset

        """
        raise NotImplementedError(f'{self.__class__.__name__!r} does not support set_bytes method')
