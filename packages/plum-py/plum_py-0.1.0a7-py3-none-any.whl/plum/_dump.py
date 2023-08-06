# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Pack/unpack memory summary."""

TAB = '  '


class Dump:

    """Pack/unpack memory summary.

    :param str indent: access description indentation
    :param str access: access description
    :param str value: memory bytes value representation
    :param bits: start, end bit offset (None -> not a bit field)
    :type bits: tuple of (int, int)
    :param list rows: summary rows

    """

    def __init__(self, indent='', access='', value='', bits=None, rows=None):
        if rows is None:
            rows = []

        rows.append(self)

        self.rows = rows

        self.indent = indent
        self.access = access
        self.value = value
        self.memory = b''
        self.cls = ''
        self.bits = bits

    def add_level(self, access='', bits=None):
        """Add row with access column value indented further.

        :param str access: access description
        :param bits: start, end bit offset (None -> not a bit field)
        :type bits: tuple of (int, int)

        """
        indent = self.indent + TAB
        return Dump(indent, access, bits=bits, rows=self.rows)

    def add_row(self, access='', value='', memory=None):
        """Add row with access column value indention at same level.

        :param str access: access description
        :param str value: memory bytes value representation
        :param bytes memory: memory bytes

        """
        row = Dump(self.indent, access, value, rows=self.rows)
        if memory is not None:
            row.memory = memory
        return row

    def add_extra_bytes(self, access, memory):
        """Add rows listing memory bytes without access/value descriptions.

        :param str access: access description
        :param bytes memory: memory bytes

        """
        for i in range(0, len(memory), 16):
            subdump = self.add_level(access=access)
            subdump.memory = memory[i:i + 16]
            access = ''

    HEADERS = ['Offset', 'Access', 'Value', 'Memory', 'Type']

    @property
    def cells(self):
        """Table row column values.

        :returns: column name/values
        :rtype: dict

        """
        try:
            pos, size = self.bits
        except TypeError:
            # bits is None
            bits = ''
        else:
            end = pos + size - 1
            if end == pos:
                bits = f'[{pos}]'
            else:
                bits = f'[{pos}:{pos + size - 1}]'

        return {
            'Offset': bits,  # byte offset prepended later
            'Access': self.indent + self.access,
            'Value': str(self.value),
            'Memory': ' '.join('{:02x}'.format(c) for c in self.memory),
            # pylint: disable=no-member
            'Type': self.cls if isinstance(self.cls, str) else self.cls.__name__,
        }

    def _get_lines(self):
        rows = list(row.cells for row in self.rows)

        # make bit offset information uniform in length
        if any(cells['Offset'] for cells in rows):
            fmt = '{:%ds}' % max(len(cells['Offset']) for cells in rows)
            for cells in rows:
                cells['Offset'] = fmt.format(cells['Offset'])

        # prepend byte offset
        nbytes = sum(len(row.memory) for row in self.rows)
        offset_template = '{:%dd}' % len(str(nbytes))
        filler = ' ' * len(str(nbytes))
        consumed = 0
        for cells, row in zip(rows, self.rows):
            if row.memory:
                byte_offset = offset_template.format(consumed)
                consumed += len(row.memory)
            else:
                byte_offset = filler
            cells['Offset'] = byte_offset + cells['Offset']

        cell_sizes = [
            max([len(name)] + [len(cells[name]) for cells in rows])
            for name in self.HEADERS]

        border = '+{}+'.format('+'.join('-' * (n + 2) for n in cell_sizes))
        row_template = '|{}|'.format('|'.join(' {:%ds} ' % n for n in cell_sizes))

        yield border
        yield row_template.format(*self.HEADERS)
        yield border
        for cells in rows:
            yield row_template.format(*cells.values())
        yield border

    def __str__(self):
        return '\n'.join(self._get_lines())

    def __eq__(self, other):
        return (other is self) or (other == str(self))

    def __ne__(self, other):
        return not self.__eq__(other)
