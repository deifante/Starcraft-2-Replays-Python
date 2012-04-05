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
        self.__archive_size                = 0
        self.__block_table_entries         = 0
        self.__block_table_offset          = 0
        self.__block_table_offset_high     = 0
        self.__extended_block_table_offset = 0
        self.__format_version              = 0
        self.__hash_table_entries          = 0
        self.__hash_table_offset           = 0
        self.__hash_table_offset_high      = 0
        self.__header_offset               = user_data.archive_header_offset
        self.__header_size                 = 0
        self.__replay_file                 = replay_file
        self.__sector_size_shift           = 0

    def read(self):
        """Read the contents of the MPQ Archive Header

        The method will replace the "read head" on the input
        file to the start of the file when done.
        """
        archive_header_struct = Struct('=3I2h4IQ2H')
        self.__replay_file.seek(self.__header_offset)
        archive_header_tuple = archive_header_struct.unpack_from(self.__replay_file.read(44))

        if ArchiveHeader.MAGIC_MPQ_VALUE != archive_header_tuple[0]:
            return False

        self.__header_size, self.__archive_size, self.__format_version, self.__sector_size_shift, \
        self.__hash_table_offset, self.__block_table_offset, self.__hash_table_entries, \
        self.__block_table_entries, self.__extended_block_table_offset, self.__hash_table_offset_high, \
        self.__block_table_offset_high = archive_header_tuple[1:]
        self.__replay_file.seek(0)
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
'''.format(self.__archive_size, self.__block_table_entries, self.__block_table_offset,
           self.__block_table_offset_high, self.__extended_block_table_offset, self.__format_version,
           self.__hash_table_entries, self.__hash_table_offset, self.__hash_table_offset_high,
           self.__header_offset, self.__header_size, self.__sector_size_shift, 512 * 2**self.__sector_size_shift)

    def get_block_table_offset(self):
        """Provide external access to the block table offset.
        Read only access.
        """
        return self.__block_table_offset

    # Read only property for the Block Table Offset
    block_table_offset = property(get_block_table_offset)

    def get_block_table_entries(self):
        """Provide external access to the number of Block Table entries.
        Read only access.
        """
        return self.__block_table_entries

    # Read only property for the Block Table Entries
    block_table_entries =  property(get_block_table_entries)
