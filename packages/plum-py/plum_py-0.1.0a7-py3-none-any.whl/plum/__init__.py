# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Classes and utilities for packing/unpacking memory bytes."""

import os

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

from ._utils import (
    calcsize,
    dump,
    exhaust,
    getbytes,
    getdump,
    getvalue,
    pack,
    pack_and_getdump,
    pack_into,
    pack_into_and_getdump,
    setvalue,
    unpack,
    unpack_and_getdump,
    unpack_from,
    unpack_from_and_getdump,
    view,
)

enable_boost = os.environ.get('ENABLE_PLUM_BOOST', 'AUTO').upper()

if enable_boost in {'AUTO', 'YES'}:  # pragma: no cover
    try:
        import plum_boost as boost
    except ImportError:
        if enable_boost == 'YES':
            raise
        boost = None
    else:
        pack = boost.pack
        pack_into = boost.pack_into
        unpack = boost.unpack
        unpack_from = boost.unpack_from

elif enable_boost == 'NO':  # pragma: no cover
    boost = None

else:  # pragma: no cover
    raise RuntimeError('ENABLE_PLUM_BOOST environment variable must be YES, NO, or AUTO')


del enable_boost, os
