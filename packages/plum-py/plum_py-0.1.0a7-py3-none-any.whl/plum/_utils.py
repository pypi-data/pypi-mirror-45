# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Plum utility functions."""

from contextlib import contextmanager
from io import BytesIO

from ._dump import Dump

from ._exceptions import (
    ExcessMemoryError,
    ImplementationError,
    InsufficientMemoryError,
    PackError,
    SizeError,
    UnpackError,
)

from ._plum import Plum
from ._plumview import PlumView
from ._plumtype import PlumType
from .memory._base_interface import MemoryInterface


def calcsize(item):
    """Get size of packed item (in bytes).

    :param items: plum type, plum type instance, or plum view
    :type items: PlumType, PlumView or Plum
    :returns: size in bytes
    :rtype: int
    :raises SizeError: if size varies with instance

    For example:

        >>> from plum import calcsize
        >>> from plum.int.little import UInt16, UInt8
        >>> calcsize(UInt8)
        1
        >>> calcsize(UInt16(0))
        2

    """
    if isinstance(item, PlumType):
        item_nbytes = item.__nbytes__
        if item_nbytes is None:
            raise SizeError(f'{item.__name__!r} instance sizes vary')

    else:
        if isinstance(item, PlumView):
            item_nbytes = item.__type__.__nbytes__
        elif isinstance(item, Plum):
            item_nbytes = type(item).__nbytes__
        else:
            raise TypeError(f'calcsize() argument must be a plum type or view')

        if item_nbytes is None:
            memory = bytearray()
            try:
                # attempt w/o dump for performance
                _pack(memory, 0, (item,), {}, None)
            except Exception:
                # do it over to include dump in exception message
                memory = bytearray()
                _pack(memory, 0, (item,), {}, Dump())
                raise ImplementationError()  # pragma: no cover
            else:
                item_nbytes = len(memory)

    return item_nbytes


def dump(item):
    """Print packed memory summary.

    :param Plum item: packable/unpacked memory item

    """
    print(getdump(item))


@contextmanager
def exhaust(memory):
    """Verify all memory bytes consumed.

    Provide context manager that verifies that all memory bytes
    were consumed in unpack operations.

    :param memory: memory to unpack
    :type memory: bytes-like (e.g. bytes, bytearray) or binary file

    """
    try:
        # create binary file from bytes or bytearray
        memory = BytesIO(memory)
    except TypeError:
        pass # must already be a binary file

    try:
        yield memory
    finally:
        extra_bytes = memory.read()
        if extra_bytes:
            msg = f'{len(extra_bytes)} unconsumed memory bytes '
            raise ExcessMemoryError(msg, extra_bytes)


def getbytes(memory, offset, nbytes, limit, dmp, cls):
    """Get memory bytes.

    :param memory: memory bytes
    :type memory: bytes-like (e.g. bytes, bytearray, etc.) or binary file
    :param int offset: offset into memory
    :param int nbytes: bytes to consume
    :param int limit: max number of bytes to consume
    :param Dump dmp: memory summary dump
    :param type cls: plum type of item that consumed bytes are for
    :returns: tuple of (memory bytes, offset, limit)
    :rtype: bytes-like, int, int or None

    """
    if limit is not None:
        nbytes = limit if (nbytes is None or (limit < nbytes)) else nbytes
        limit -= nbytes

    if nbytes is None:
        try:
            chunk = memory[offset:]
        except TypeError:
            chunk = memory.read()
        else:
            offset += len(chunk)

        if dmp:
            dmp.cls = cls
            dmp.memory = chunk

    else:
        start = offset
        offset += nbytes
        try:
            chunk = memory[start: offset]
        except TypeError:
            chunk = memory.read(nbytes)

        if len(chunk) < nbytes:
            if dmp:
                dmp.cls = cls
                dmp.value = '<insufficient bytes>'
                if len(chunk) > 16:
                    dmp.add_extra_bytes('', chunk)
                else:
                    dmp.memory = chunk

            cls_name = '' if cls is None else f'{cls.__name__} '

            unpack_shortage = (
                f'{nbytes - len(chunk)} too few memory bytes to unpack {cls_name}'
                f'({nbytes} needed, only {len(chunk)} available)')

            raise InsufficientMemoryError(unpack_shortage)

        if dmp:
            dmp.cls = cls
            dmp.memory = chunk

    return chunk, offset, limit


def getdump(item):
    """Get packed memory summary.

    :param Plum item: packable/unpacked memory item
    :param str name: item name (for ``access`` column)
    :returns: summary table of view detailing memory bytes and layout
    :rtype: str

    """
    dmp = Dump()
    _pack(bytearray(), 0, (item,), {}, dmp)
    dmp.access = 'x'
    return dmp


def getvalue(plumview):
    """Unpack item from memory bytes of a plum view.

    For example, the following unpacks an integer from a USInt8 plum view:

        >>> from plum import getvalue, view
        >>> from plum.memory import LocalMemory
        >>> from plum.int.little import UInt8
        >>> memory = LocalMemory(b'\x00\xff\x00')
        >>> value = view(UInt8, memory, offset=1)
        >>> getvalue(value)
        255

    :param PlumView plumview: data memory view
    :returns: unpacked item
    :rtype: object

    """
    if not isinstance(plumview, PlumView):
        raise TypeError('getvalue() argument must be a plum view')

    return plumview.__getvalue__()


def _pack(memory, offset, items, kwargs, dmp):
    # pylint: disable=too-many-branches, too-many-nested-blocks
    try:
        cls = None
        i = 0
        for item in items:
            if isinstance(item, PlumType):
                if cls is None:
                    cls = item
                else:
                    raise TypeError('plum type specified without a value')
            else:
                if dmp:
                    if dmp.access:
                        dmp = dmp.add_row(access=f'[{i}]')
                    else:
                        dmp.access = f'[{i}]'
                if cls is None:
                    if isinstance(item, PlumView):
                        cls = item.__type__
                    else:
                        cls = type(item)
                        if not isinstance(cls, PlumType):
                            raise TypeError('value specified without a plum type')
                offset = cls.__pack__(memory, offset, item, dmp)
                i += 1
                cls = None

        if cls is not None:
            raise TypeError('plum type specified without a value')

        if kwargs:
            for name, item in kwargs.items():
                if dmp:
                    if dmp.access:
                        dmp = dmp.add_row(access=name)
                    else:
                        dmp.access = name
                if isinstance(item, Plum):
                    offset = item.__pack__(memory, offset, item, dmp)
                else:
                    if isinstance(item, PlumView):
                        offset = item.__type__.__pack__(memory, offset, item, dmp)
                    else:
                        raise TypeError('value specified without a plum type')

    except Exception as exc:
        if dmp:
            raise PackError(
                f"\n\n{dmp if dmp else '<no dump table yet>'}"
                f"\n\nPackError: unexpected {type(exc).__name__} "
                f"exception occurred during pack operation, dump "
                f"above shows interrupted progress, original "
                f"exception traceback appears above this exception's "
                f"traceback"
            ).with_traceback(exc.__traceback__)

        raise


def pack(*items, **kwargs):
    r"""Pack items and return memory bytes.

    For example:

        >>> from plum import pack
        >>> from plum.int.little import UInt8, UInt16
        >>> pack(UInt8(1), UInt16(2))
        bytearray(b'\x01\x02\x00')
        >>> pack(UInt8, 1, UInt16, 2)
        bytearray(b'\x01\x02\x00')
        >>> pack(m1=UInt8(1), m2=UInt16(2))
        bytearray(b'\x01\x02\x00')

    :param items: packable/unpacked memory items
    :type items: Plum (e.g. UInt8, Array, etc.)
    :param kwargs: packable/unpacked memory items
    :type kwargs: dict of plum instances
    :returns: memory bytes
    :rtype: bytearray

    """
    memory = bytearray()
    try:
        # attempt w/o dump for performance
        _pack(memory, 0, items, kwargs, None)
    except Exception:
        # do it over to include dump in exception message
        _pack(memory, 0, items, kwargs, Dump())
        raise ImplementationError()  # pragma: no cover

    return memory


def pack_and_getdump(*items, **kwargs):
    """Pack items and return memory bytes and summary.

    :param items: packable/unpacked memory items
    :type items: tuple of plum types/values
    :param kwargs: packable/unpacked memory items
    :type kwargs: dict of plum instances
    :returns: memory bytes, packed memory summary
    :rtype: bytearray, Dump

    """
    memory = bytearray()
    dmp = Dump()
    _pack(memory, 0, items, kwargs, dmp)
    return memory, dmp


def pack_into(buffer, offset, *items, **kwargs):
    r"""Pack items into memory bytes.

    For example:

        >>> from io import BytesIO
        >>> from plum import pack_into
        >>> from plum.int.little import UInt8
        >>>
        >>> memory = bytearray(b'\x00\x00\x00')
        >>> pack_into(memory, 1, UInt8, 1)
        >>> memory
        bytearray(b'\x00\x01\x00')
        >>>
        >>> memory = BytesIO(b'\x00\x00\x00')
        >>> pack_into(memory, 1, UInt8(1))
        >>> memory.seek(0)
        0
        >>> memory.read()
        b'\x00\x01\x00'
        >>>
        >>> memory = bytearray(b'\x00\x00\x00\x00')
        >>> pack_into(memory, 1, m1=UInt8(1), m2=UInt8(2))
        >>> memory
        bytearray(b'\x00\x01\x02\x00')

    :param buffer: memory byte buffer
    :type buffer: writeable bytes-like object or binary file
    :param int offset: byte offset into memory byte buffer
    :param items: packable/unpacked memory items
    :type items: Plum (e.g. UInt8, Array, etc.)
    :param kwargs: packable/unpacked memory items
    :type kwargs: dict of plum instances

    """
    if isinstance(buffer, bytearray):
        memory = buffer
        _offset = offset
    else:
        memory = bytearray()
        _offset = 0

    try:
        # attempt w/o dump for performance
        _pack(memory, _offset, items, kwargs, None)
    except Exception:
        # do it over to include dump in exception message
        _pack(memory, _offset, items, kwargs, Dump())
        raise ImplementationError()  # pragma: no cover

    if memory is not buffer:
        try:
            buffer[offset:offset + len(memory)] = memory
        except TypeError:
            buffer.seek(offset)
            buffer.write(memory)


def pack_into_and_getdump(buffer, offset, *items, **kwargs):
    r"""Pack items into memory bytes and return memory summary.

    For example:

        >>> from io import BytesIO
        >>> from plum import pack_into
        >>> from plum.int.little import UInt8
        >>>
        >>> memory = bytearray(b'\x00\x00\x00')
        >>> pack_into(memory, 1, UInt8, 1)
        >>> memory
        bytearray(b'\x00\x01\x00')
        >>>
        >>> memory = BytesIO(b'\x00\x00\x00')
        >>> pack_into(memory, 1, UInt8(1))
        >>> memory.seek(0)
        0
        >>> memory.read()
        b'\x00\x01\x00'
        >>>
        >>> memory = bytearray(b'\x00\x00\x00\x00')
        >>> pack_into(memory, 1, m1=UInt8(1), m2=UInt8(2))
        >>> memory
        bytearray(b'\x00\x01\x02\x00')

    :param buffer: memory byte buffer
    :type buffer: writeable bytes-like object or binary file
    :param items: packable/unpacked memory items
    :type items: Plum (e.g. UInt8, Array, etc.)
    :param kwargs: packable/unpacked memory items
    :type kwargs: dict of plum instances
    :returns: packed memory summary
    :rtype: Dump

    """
    if isinstance(buffer, bytearray):
        memory = buffer
        _offset = offset
    else:
        memory = bytearray()
        _offset = 0

    dmp = Dump()

    _pack(memory, _offset, items, kwargs, dmp)

    if memory is not buffer:
        try:
            buffer[offset:offset + len(memory)] = memory
        except TypeError:
            buffer.seek(offset)
            buffer.write(memory)

    return dmp


def setvalue(plumview, value):
    """Pack value into memory bytes of a plum view.

    For example:
        >>> from plum import setvalue, view
        >>> from plum.memory import LocalMemory
        >>> from plum.int.little import UInt8
        >>> memory = LocalMemory(bytearray([0x00, 0xFF, 0x00]))
        >>> view = view(UInt8, memory, offset=1)
        >>> setvalue(view, 1)
        >>> memory
        LocalMemory([0, 1, 0])

    :param PlumView plumview: data memory view
    :param object value: new value

    """
    if not isinstance(plumview, PlumView):
        raise TypeError('setvalue() argument must be a plum view')

    plumview.__setvalue__(value)


def unpack(cls, memory):
    r"""Unpack item from memory bytes.

    For example:
        >>> from plum import unpack
        >>> from plum.int.little import UInt16
        >>> unpack(UInt16, b'\x01\x02')
        513

    :param PlumClass cls: plum type, e.g. ``UInt16``
    :param memory: memory bytes
    :type memory: bytes-like (e.g. bytes, bytearray, etc.)
    :returns: plum instance
    :rtype: cls

    """
    try:
        item, offset, _limit = cls.__unpack__(memory, 0, None, None, None)
    except Exception:
        # do it over to include dump in exception message
        unpack_and_getdump(cls, memory)
        raise ImplementationError()  # pragma: no cover

    extra_bytes = memory[offset:]

    if extra_bytes:
        # do it over to include dump in exception message
        dmp = Dump(access='x')

        try:
            cls.__unpack__(memory, 0, None, dmp, None)
        except Exception:  # pragma: no cover
            raise ImplementationError()

        for i in range(0, len(extra_bytes), 16):
            dmp.add_row(access='<excess memory>', memory=extra_bytes[i:i+16])

        msg = (
            f'\n\n{dmp}\n\n'
            f'{len(extra_bytes)} unconsumed memory bytes '
        )

        raise ExcessMemoryError(msg, extra_bytes)

    return item


def unpack_and_getdump(cls, memory):
    """Unpack item from memory bytes and get packed memory summary.

    For example:
        >>> from plum import unpack_and_getdump
        >>> from plum.int.little import UInt16
        >>> x, dmp = unpack_and_getdump(UInt16, b'\x01\x02')
        >>> x
        513
        >>> print(dmp)
        +--------+--------+-------+--------+--------+
        | Offset | Access | Value | Memory | Type   |
        +--------+--------+-------+--------+--------+
        | 0      | x      | 513   | 01 02  | UInt16 |
        +--------+--------+-------+--------+--------+

    :param Plum cls: plum type, e.g. ``UInt16``
    :param memory: memory bytes
    :type memory: bytes-like (e.g. bytes, bytearray, etc.)
    :returns: tuple of (plum instance, summary)
    :rtype: (cls, str)

    """
    dmp = Dump(access='x')

    try:
        item, offset, _limit = cls.__unpack__(memory, 0, None, dmp, None)

    except InsufficientMemoryError as exc:
        raise InsufficientMemoryError(
            f'\n\n{dmp}\n\nInsufficientMemoryError: {exc}, '
            f'dump above shows interrupted progress',
            *exc.args[1:]).with_traceback(exc.__traceback__)

    except Exception as exc:
        raise UnpackError(
            f"\n\n{dmp}"
            f"\n\nUnpackError: unexpected {type(exc).__name__} "
            f"exception occurred during unpack operation, "
            f"dump above shows interrupted progress, original "
            f"exception traceback appears above this exception's "
            f"traceback"
        ).with_traceback(exc.__traceback__)

    extra_bytes = memory[offset:]

    if extra_bytes:
        for i in range(0, len(extra_bytes), 16):
            dmp.add_row(access='<excess memory>', memory=extra_bytes[i:i+16])

        msg = (
            f'\n\n{dmp}\n\n'
            f'{len(extra_bytes)} unconsumed memory bytes '
        )

        raise ExcessMemoryError(msg, extra_bytes)

    return item, dmp


def unpack_from(cls, memory, offset=None):
    r"""Unpack item from memory bytes.

    For example:
        >>> from io import BytesIO
        >>> from plum import unpack_from
        >>> from plum.int.little import UInt8
        >>> unpack_from(UInt8, BytesIO(b'\x99\x01\x99'), offset=1)
        1

    :param PlumClass cls: plum type, e.g. ``UInt16``
    :param memory: memory bytes
    :type memory: binary file
    :param int offset: starting byte offset
    :returns: plum instance
    :rtype: cls

    """
    if offset is None:
        offset = memory.tell()
    else:
        memory.seek(offset)

    try:
        item, _offset, _limit = cls.__unpack__(memory, offset, None, None, None)
    except Exception:
        # do it over to include dump in exception message
        memory.seek(offset)
        unpack_from_and_getdump(cls, memory, offset)
        raise ImplementationError()  # pragma: no cover

    return item


def unpack_from_and_getdump(cls, memory, offset=None):
    """Unpack item from memory bytes and get packed memory summary.

    For example:
        >>> from io import BytesIO
        >>> from plum import unpack_from_and_getdump
        >>> from plum.int.little import UInt8
        >>> x, d = unpack_from_and_getdump(UInt8, BytesIO(b'\x99\x01\x99'), offset=1)
        >>> x
        1
        >>> print(d)
        +--------+--------+-------+--------+-------+
        | Offset | Access | Value | Memory | Type  |
        +--------+--------+-------+--------+-------+
        | 0      | x      | 1     | 01     | UInt8 |
        +--------+--------+-------+--------+-------+

    :param Plum cls: plum type, e.g. ``UInt16``
    :param memory: memory bytes
    :type memory: binary file
    :param int offset: starting byte offset (default to current position)
    :returns: tuple of (plum instance, summary)
    :rtype: (cls, str)

    """
    dmp = Dump(access='x')

    if offset is None:
        offset = memory.tell()
    else:
        memory.seek(offset)

    try:
        item, _offset, _limit = cls.__unpack__(memory, offset, None, dmp, None)

    except InsufficientMemoryError as exc:
        raise InsufficientMemoryError(
            f'\n\n{dmp}\n\nInsufficientMemoryError: {exc}, '
            f'dump above shows interrupted progress',
            *exc.args[1:]).with_traceback(exc.__traceback__)

    except Exception as exc:
        raise UnpackError(
            f"\n\n{dmp}"
            f"\n\nUnpackError: unexpected {type(exc).__name__} "
            f"exception occurred during unpack operation, "
            f"dump above shows interrupted progress, original "
            f"exception traceback appears above this exception's "
            f"traceback"
        ).with_traceback(exc.__traceback__)

    return item, dmp


def view(plumtype, memory, offset=0):
    """Create plum view of memory bytes.

    For example:
        >>> from plum import view
        >>> from plum.memory import LocalMemory
        >>> from plum.int.little import UInt16
        >>> memory = LocalMemory(b'\x01\x02\x03\x04')
        >>> value = view(UInt16, memory, offset=1)
        >>> value
        IntView(770)
        >>> value == 770
        True

    :param PlumType plumtype: plum type to view
    :param MemoryInterface memory: memory bytes
    :param int offset: byte offset

    """
    if not isinstance(plumtype, PlumType):
        raise TypeError(f'{plumtype!r} is not a plum type')

    if not isinstance(memory, MemoryInterface):
        raise TypeError('view function requires memory interface to view')

    return plumtype.__view__(plumtype, memory, offset)
