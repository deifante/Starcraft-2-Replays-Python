from struct import *

class ArchiveHeader(object):
    """Reads the archive header of the sc2 replay files."""

    # This magic value is to be found as the first four bytes of
    # a valid archive header
    MAGIC_MPQ_VALUE = 441536589 # MPQ0x1A

    def __init__(self, replay_file, user_data):
        """Instantiate a header reading object.

        Keyword arguments:
        replay_file -- The already opened replay file.
        header_offset -- The number of bytes from the start of the file to the start of the Archive Header block.
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
        self.__replay_file.seek(self.__header_offset)
        magic_file_id = unpack('=I', self.__replay_file.read(4))[0]

        if ArchiveHeader.MAGIC_MPQ_VALUE != magic_file_id:
            return False

        self.__header_size, self.__archive_size = unpack('=II', self.__replay_file.read(8))
        self.__format_version, self.__sector_size_shift = unpack('=hB', self.__replay_file.read(3))
        self.__hash_table_offset, self.__block_table_offset, self.__hash_table_entries = \
            unpack('=III', self.__replay_file.read(12))
        self.__block_table_entries = unpack('=I', self.__replay_file.read(4))[0]
        self.__extended_block_table_offset, self.__hash_table_offset_high, self.__block_table_offset_high = \
            unpack('=QHH', self.__replay_file.read(12))
        self.__replay_file.seek(0)

    def __str__(self):
        return '''MPQ Archive Header
    Archive Size                : %u bytes
    Block Table Entries         : %u bytes
    Block Table Offset          : %u bytes
    Block Table Offset High     : %u bytes
    Extended Block Table Offset : %u bytes
    Format Version              : %u bytes
    Hash Table Entries          : %u bytes
    Hash Table Offset           : %u bytes
    Hash Table Offset High      : %u bytes
    Header Offset               : %u bytes
    Header Size                 : %u bytes
    Sector Size Shift           : %u bytes ''' % \
            (self.__archive_size, self.__block_table_entries, self.__block_table_offset,\
                 self.__block_table_offset_high, self.__extended_block_table_offset, self.__format_version,\
                 self.__hash_table_entries, self.__hash_table_offset, self.__hash_table_offset_high,\
                 self.__header_offset, self.__header_size, self.__sector_size_shift)
