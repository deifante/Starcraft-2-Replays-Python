from struct import *

class ArchiveHeader:
    """Reads the archive header of the sc2 replay files."""

    STARCRAFT_2_BUFFER            = 0x400
    STARCRAFT_2_MAGIC_NAME        = 'StarCraft II replay'
    STARCRAFT_2_MAGIC_NAME_OFFSET = 0x15
    STARCRAFT_2_MPQ_VALUE         = 458313805
    MAGIC_MPQ_VALUE               = 441536589 #MPQ0x1A

    def __init__(self, file_name):
        """Instantiate a header reading object.
        Keyword arguments:
        file_name -- the full path of the file. May be relative or absolute.
        """
        self.file_name = file_name
        self.header_size = 0
        self.archive_size = 0

    def verify_file(self):
        """Verify that this is, in fact, a Starcraft 2 replay file."""
        replay_file = open(self.file_name, 'rb')
        magic_sc2_value = unpack('=i', replay_file.read(4))[0]
        # Not exactly sure how this one works right now, but it's an
        # "almost MPQ" magic file indicator. This one ends with 0x1b
        # instead of 0x1a.
        if ArchiveHeader.STARCRAFT_2_MPQ_VALUE != magic_sc2_value:
            replay_file.close()
            return False

        replay_file.seek(ArchiveHeader.STARCRAFT_2_MAGIC_NAME_OFFSET)
        replay_type = replay_file.read(len(ArchiveHeader.STARCRAFT_2_MAGIC_NAME))
        if replay_type != ArchiveHeader.STARCRAFT_2_MAGIC_NAME:
            replay_file.close()
            return False

        replay_file.seek(ArchiveHeader.STARCRAFT_2_BUFFER)
        magic_value = unpack('=i', replay_file.read(4))[0]

        replay_file.close()
        if ArchiveHeader.MAGIC_MPQ_VALUE != magic_value:
            return False
        return True

    def read(self):
        """Read the contents of the MPQ Archive Header"""
        replay_file = open(self.file_name, 'rb')
        # Skip the magic file indicatior @ the start of the file
        replay_file.seek(ArchiveHeader.STARCRAFT_2_BUFFER + 4)

        self.header_size, self.archive_size = unpack('=II', replay_file.read(8))
        print 'header_size', self.header_size
        print 'archive_size', self.archive_size

        self.format_version, self.sector_size_shift = unpack('=hB', replay_file.read(3))
        print 'format_version', self.format_version
        print 'sector_size_shift', self.sector_size_shift

        self.hash_table_offset, self.block_table_offset, self.hash_table_entries = \
            unpack('=III', replay_file.read(12))
        print 'hash_table_offset', self.hash_table_offset
        print 'block_table_offset', self.block_table_offset
        print 'hash_table_entries', self.hash_table_entries

        self.block_table_entries = unpack('=I', replay_file.read(4))[0]
        print 'block_table_entries', self.block_table_entries

        # The following fields are only present after The Burning Crusade
        self.extended_block_table_offset, self.hash_table_offset_high, self.block_table_offset_high = \
            unpack('=QHH', replay_file.read(12))
        print 'extended_block_table_offset', self.extended_block_table_offset
        print 'hash_table_offset_high', self.hash_table_offset_high
        print 'block_table_offset_high', self.block_table_offset_high

        replay_file.close()

if __name__ == "__main__":
    header = ArchiveHeader('samples/Victory-of-the-Year.SC2Replay')
    if header.verify_file():
        print 'Valid File'
        header.read()
    else:
        print 'Not valid file'
