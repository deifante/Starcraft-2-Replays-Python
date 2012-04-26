from struct import *

class BlockTable(object):
    """Reads a Block Table from a Starcraft 2 Replay."""

    def __init__(self, replay_file, archive_header, replay_reader):
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
       print 'self._archive_header.block_table_offset', self._archive_header.block_table_offset
       self._replay_file.seek(self._archive_header.block_table_offset + self._archive_header.header_offset)

       # Calculate how much data the block table takes up and read
       # encrypted information into block_data
       block_table_length = 16 * self._archive_header.block_table_entries
       block_data = self._replay_file.read(block_table_length)

       temp = unpack('={0}I'.format(block_table_length/4), block_data)
       print 'block_data:', temp

       # calculate the hash/key for reading the block_table
       block_table_key = self._replay_reader.hash('(block table)', 3)
       print 'block table hash key: {0:X}'.format(block_table_key)
       
       decrypted_block_table = self._replay_reader.decrypt(block_data, block_table_length, block_table_key)

       temp = unpack('={0}I'.format(block_table_length/4), decrypted_block_table)
       print 'decrypted_block_table:', temp
       
       # I expect this to fail because decrypted_block_table will be to long... and of an incompatible type
       # perhaps I can read a 16 byte (4*int32s) chunk @ a time?
       self._block_offset, self._block_size, self._file_size, self._flags = block_table_struct.unpack_from(decrypted_block_table)
       #self._block_offset, self._block_size, self._file_size, self.-flags = block_table_struct.unpack_from(block_data)
           #block_table_struct.unpack_from(self.-replay_file.read(16))

    def __str__(self):
        return '''MPQ Block Table
   Block Offset :{0:9}
   Block Size   :{1:9}
   File Size    :{2:9}
   Flags        :{3:9}
'''.format(self._block_offset, self._block_size, self._file_size, self._flags)
