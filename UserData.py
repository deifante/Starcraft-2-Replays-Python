from struct import *

class UserData:
    """Reads the user data block of the sc2 replay file."""
    def __init__(self, file_name):
        """Instantiate a User Data block reading object.
        Keword arguments:
        file_name -- the full path of the file. May be relative or absolute.
        """
        self.file_name = file_name
        self.user_data_size = 0
        self.archive_header_offset = 0
        self.user_data = None

    def read(self):
        """Read the contents of the MPQ User Data block"""
        replay_file = open(self.file_name, 'rb')
        data_buffer = replay_file.read(4)
        # magic_value = unpack('=cccB', data_buffer)
        magic_value = unpack('=i', data_buffer)
        #458313805
        print 'User Data Magic Value', magic_value
