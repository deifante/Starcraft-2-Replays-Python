from struct import *

class ArchiveHeader(object):
    """Reads the archive header of the sc2 replay files."""

    MAGIC_MPQ_VALUE = 441536589 #MPQ0x1A
    def __init__(self, replay_file, header_offset):
        """Instantiate a header reading object.
        Keyword arguments:
        file_name -- the full path of the file. May be relative or absolute.
        header_offset -- distance from the start of the file to the start of the Archive Header block
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
        self.__header_offset               = header_offset
        self.__header_size                 = 0
        self.__replay_file                 = replay_file
        self.__sector_size_shift           = 0
        self.__replay_file.seek(0)        

    def read(self):
        """Read the contents of the MPQ Archive Header
        Replace the "read head" on the input file to the start of the file when done.
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
        return 'MPQ Archive Header'

if __name__ == "__main__":
    header = ArchiveHeader('samples/Victory-of-the-Year.SC2Replay')
    header.read()
    # if header.verify_file():
    #     print 'Valid File'
    #     header.read()
    # else:
    #     print 'Not valid file'
