from struct import Struct
from collections import namedtuple

class BlockTable(object):
    """Reads a Block Table from a Starcraft 2 Replay."""
    BlockTableTuple = namedtuple('BlockTableTuple', 'block_offset block_size file_size flags')
    IS_FILE            = 0x80000000
    HAS_CHECKSUM       = 0x04000000
    IS_DELETION_MARKER = 0x02000000
    IS_SINGLE_UNIT     = 0x01000000
    IS_KEY_ADJUSTED    = 0x00020000
    IS_ENCRYPTED       = 0x00010000
    IS_COMPRESSED      = 0x00000200
    IS_IMPLODED        = 0x00000100

    def __init__(self, replay_file, archive_header, replay_reader):
        """Instantiate a block table reading object.

        Keyword arguments:
        replay_file -- The already opened replay file.
        archive_header -- Archive Header information from the same replay file.
        """
        self._tables         = []
        self._archive_header = archive_header
        self._replay_file    = replay_file
        self._replay_reader  = replay_reader

    def read(self):
       """Read the contents of the encrypted MPQ Block Table.

       The method will replace the "read head" on the input
       file to the start of the file when done.
       """
       # define basic structure of the block table entry
       block_table_struct = Struct('=4I')
       # go to the first entry
       self._replay_file.seek(self._archive_header.block_table_offset + self._archive_header.header_offset)

       # Calculate how much data the block table takes up and read
       # encrypted information into block_data
       block_table_length = 16 * self._archive_header.block_table_entries
       block_data = self._replay_file.read(block_table_length)

       # calculate the hash/key for reading the block_table
       block_table_key = self._replay_reader.hash('(block table)', 3)
       decrypted_block_table = self._replay_reader.decrypt(block_data, block_table_length, block_table_key)

       for i in range(self._archive_header.block_table_entries):
           self._tables.append(BlockTable.BlockTableTuple._make(
                   block_table_struct.unpack_from(decrypted_block_table[16*i:])))
       self._replay_file.seek(0)

    def print_flags(self, flags):
        accumulator = ''
        if flags & BlockTable.IS_FILE:
            accumulator += 'Is File '
        if flags & BlockTable.HAS_CHECKSUM:
            accumulator += 'Has Checksum '
        if flags & BlockTable.IS_DELETION_MARKER:
            accumulator += 'Is Deletion Marker '
        if flags & BlockTable.IS_SINGLE_UNIT:
            accumulator += 'Is Single Unit '
        if flags & BlockTable.IS_KEY_ADJUSTED:
            accumulator += 'Key is Adjusted '
        if flags & BlockTable.IS_ENCRYPTED:
            accumulator += 'Is Encrypted '
        if flags & BlockTable.IS_COMPRESSED:
            accumulator += 'Is Compressed '
        if flags & BlockTable.IS_IMPLODED:
            accumulator += 'Is Imploded '
        return accumulator

    def __str__(self):
        accumulator = ''
        for table in self._tables:
            accumulator += '''MPQ Block Table
   Block Offset :{0:9}
   Block Size   :{1:9}
   File Size    :{2:9}
   Flags        :{3:9} ({4})

'''.format(table.block_offset, table.block_size, table.file_size, table.flags, self.print_flags(table.flags))
        return accumulator
