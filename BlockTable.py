from struct import *

class BlockTable(object):
    """Reads a Block Table from a Starcraft 2 Replay."""

    def __init__(self, replay_file, archive_header):
        """Instantiate a block table reading object.

        Keyword arguments:
        replay_file -- The already opened replay file.
        archive_header -- Archive Header information from the same replay file.
        """
        self._block_offset = 0
        self._block_size   = 0
        self._file_size    = 0
        self._flags        = 0

        self._archive_header = archive_header
        self._replay_file = replay_file

    def read(self):
        block_table_struct = Struct('=4I')
        self._replay_file.seek(self._archive_header.block_table_offset)
        self._block_offset, self._block_size, self._file_size, self._flags = \
            block_table_struct.unpack_from(self._replay_file.read(16))

    def __str__(self):
        return '''MPQ Block Table
   Block Offset :{0:9}
   Block Size   :{1:9}
   File Size    :{2:9}
   Flags        :{3:9}
'''.format(self._block_offset, self._block_size, self._file_size, self._flags)
