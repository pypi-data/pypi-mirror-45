# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Float type view."""

from numbers import Real

from plum import unpack, pack
from plum._plumview import NumberView


class FloatView(NumberView, Real):

    """Float type view."""

    def __eq__(self, other):
        return self.__memory__.get_bytes(
            self.__type__.__nbytes__, offset=self.__offset__) == pack(self.__type__, other)

    def __getvalue__(self):
        """Unpack float from underlying memory."""
        return unpack(self.__type__, self.__memory__.get_bytes(
            self.__type__.__nbytes__, offset=self.__offset__))

    __float__ = __getvalue__

    def __setvalue__(self, value):
        """Pack value into underlying memory.

        :param object value: new value

        """
        self.__memory__.set_bytes(pack(self.__type__, value), offset=self.__offset__)
