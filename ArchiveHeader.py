from struct import Struct

class ArchiveHeader(object):
    """Reads the archive header of the sc2 replay files."""

    # This magic value is to be found as the first four bytes of
    # a valid archive header
    MAGIC_MPQ_VALUE = 441536589 # MPQ0x1A

    def __init__(self, replay_file, user_data):
        """Instantiate a header reading object.

        Keyword arguments:
        replay_file -- The already opened replay file.
        user_data -- User Data information from the same replay file.
        """
        self._archive_size                = 0
        self._block_table_entries         = 0
        self._block_table_offset          = 0
        self._block_table_offset_high     = 0
        self._extended_block_table_offset = 0
        self._format_version              = 0
        self._hash_table_entries          = 0
        self._hash_table_offset           = 0
        self._hash_table_offset_high      = 0
        self._header_offset               = user_data.archive_header_offset
        self._header_size                 = 0
        self._replay_file                 = replay_file
        self._sector_size_shift           = 0

    def read(self):
        """Read the contents of the MPQ Archive Header

        The method will replace the "read head" on the input
        file to the start of the file when done.
        """
        archive_header_struct = Struct('=3I2H4IQ2H')
        self._replay_file.seek(self._header_offset)
        archive_header_tuple = archive_header_struct.unpack_from(self._replay_file.read(44))

        if ArchiveHeader.MAGIC_MPQ_VALUE != archive_header_tuple[0]:
            return False

        self._header_size, self._archive_size, self._format_version, self._sector_size_shift, \
        self._hash_table_offset, self._block_table_offset, self._hash_table_entries, \
        self._block_table_entries, self._extended_block_table_offset, self._hash_table_offset_high, \
        self._block_table_offset_high = archive_header_tuple[1:]
        self._replay_file.seek(0)
        return True

    def __str__(self):
        return '''MPQ Archive Header
    Archive Size                : {0:9} bytes
    Block Table Entries         : {1:9} entries
    Block Table Offset          : {2:9} bytes
    Block Table Offset High     : {3:9} bytes
    Extended Block Table Offset : {4:9} bytes
    Format Version              : {5:9}
    Hash Table Entries          : {6:9} entries
    Hash Table Offset           : {7:9} bytes
    Hash Table Offset High      : {8:9} bytes
    Header Offset               : {9:9} bytes
    Header Size                 : {10:9} bytes
    Sector Size Shift           : {11} => ({12} bytes)
'''.format(self._archive_size, self._block_table_entries, self._block_table_offset,
           self._block_table_offset_high, self._extended_block_table_offset, self._format_version,
           self._hash_table_entries, self._hash_table_offset, self._hash_table_offset_high,
           self._header_offset, self._header_size, self._sector_size_shift, 512 * 2**self._sector_size_shift)

    def get_block_table_offset(self):
        """Provide external access to the block table offset.
        Read only access.
        """
        return self._block_table_offset

    # Read only property for the Block Table Offset
    block_table_offset = property(get_block_table_offset)

    def get_block_table_entries(self):
        """Provide external access to the number of Block Table entries.
        Read only access.
        """
        return self._block_table_entries

    # Read only property for the Block Table Entries
    block_table_entries =  property(get_block_table_entries)

    def get_header_offset(self):
        """Provide external access to the header offset.
        Read only access.
        """
        return self._header_offset

    # Read only property for the Block Table Offset
    header_offset = property(get_header_offset)
