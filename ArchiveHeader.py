from struct import Struct
from collections import namedtuple

class ArchiveHeader(object):
    """Reads the archive header of the sc2 replay files."""
    ArchiveHeaderTuple = namedtuple('ArchiveHeaderTuple',
                                    ['magic', 'header_size', 'archive_size','format_version',
                                     'sector_size_shift', 'hash_table_offset', 'block_table_offset',
                                     'hash_table_entries', 'block_table_entries',
                                     'extended_block_table_offset', 'hash_table_offset_high',
                                     'block_table_offset_high'])

    # This magic value is to be found as the first four bytes of
    # a valid archive header
    MAGIC_MPQ_VALUE = 441536589 # MPQ0x1A

    def __init__(self, replay_file, user_data):
        """Instantiate a header reading object.

        Keyword arguments:
        replay_file -- The already opened replay file.
        user_data -- User Data information from the same replay file.
        """
        self._archive_header = None
        self._replay_file    = replay_file
        self._header_offset  = user_data.archive_header_offset

    def read(self):
        """Read the contents of the MPQ Archive Header

        The method will replace the "read head" on the input
        file to the start of the file when done.
        """
        archive_header_struct = Struct('=3I2H4IQ2H')
        self._replay_file.seek(self._header_offset)
        self._archive_header = ArchiveHeader.ArchiveHeaderTuple._make(
            archive_header_struct.unpack_from(self._replay_file.read(44)))

        if ArchiveHeader.MAGIC_MPQ_VALUE != self._archive_header.magic:
            return False

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
'''.format(self._archive_header.archive_size, self._archive_header.block_table_entries,
           self._archive_header.block_table_offset, self._archive_header.block_table_offset_high,
           self._archive_header.extended_block_table_offset, self._archive_header.format_version,
           self._archive_header.hash_table_entries, self._archive_header.hash_table_offset,
           self._archive_header.hash_table_offset_high, self._header_offset,
           self._archive_header.header_size,
           self._archive_header.sector_size_shift, 512 * 2**self._archive_header.sector_size_shift)

    def get_block_table_offset(self):
        """Provide external access to the block table offset.
        Read only access.
        """
        return self._archive_header.block_table_offset

    # Read only property for the Block Table Offset
    block_table_offset = property(get_block_table_offset)

    def get_block_table_entries(self):
        """Provide external access to the number of Block Table entries.
        Read only access.
        """
        return self._archive_header.block_table_entries

    # Read only property for the Block Table Entries
    block_table_entries =  property(get_block_table_entries)

    def get_header_offset(self):
        """Provide external access to the header offset.
        Read only access.
        """
        return self._header_offset

    # Read only property for the Block Table Offset
    header_offset = property(get_header_offset)
