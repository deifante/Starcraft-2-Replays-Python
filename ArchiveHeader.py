from struct import *
class ArchiveHeader:
    """Reads the archive header of the sc2 replay files."""
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
        data_buffer = replay_file.read(4)
        magic_value = unpack('=i', data_buffer)[0]

        replay_file.close()
        # First 4 bytes are M, P, Q, 0x1b
        if 458313805 != magic_value:
            return False
        return True

    def read(self):
        """Read the contents of the MPQ Archive Header"""
        replay_file = open(self.file_name, 'rb')
        # Skip the magic file indicatior @ the start of the file
        replay_file.seek(4)

        self.header_size, self.archive_size = unpack('=ii', replay_file.read(8))
        print 'header_size', self.header_size
        print 'archive_size', self.archive_size

        self.format_version = unpack('=h', replay_file.read(2))[0]
        print 'format_version', self.format_version
        replay_file.close()

if __name__ == "__main__":
    header = ArchiveHeader('samples/Victory-of-the-Year.SC2Replay')
    if header.verify_file():
        print 'Valid File'
        header.read()
