from struct import *

class UserData(object):
    """Reads the user data block of the MPQ file."""

    # This magic value is to be found as the first four bytes of
    # a valid user data block
    STARCRAFT_2_USER_DATA_MAGIC_VALUE = 458313805 # MPQ0x1B
    STARCRAFT_2_MAGIC_NAME            = 'StarCraft II replay'
    USER_DATA_UNKNOWN_BLOCK_SIZE_0    = 9

    def __init__(self, replay_file):
        """Instantiate a User Data block reading object.

        Keword arguments:
        replay_file -- The already opened replay file.
        """
        self.__replay_file           = replay_file
        self.__user_data             = None
        self.__archive_header_offset = 0
        self.__user_data_size        = 0
        # Not really sure about the following data.
        self.__major_version         = {'Initial Release':0, 'Patch':0}
        self.__build_number          = 0

    def read(self):
        """"Verify that the User Data block is as expected.
        Replace the "read head" on the input file to the start of the file.
        """
        data_buffer = self.__replay_file.read(4)
        magic_value = unpack('=i', data_buffer)[0]
        if UserData.STARCRAFT_2_USER_DATA_MAGIC_VALUE != magic_value:
            self.__replay_file.close()
            return False

        self.__user_data_size, self.__archive_header_offset = unpack('=II', self.__replay_file.read(8))
        self.__user_data = self.__replay_file.read(self.__user_data_size)

        sc2_user_data_replay = self.__user_data[
            UserData.USER_DATA_UNKNOWN_BLOCK_SIZE_0:
                UserData.USER_DATA_UNKNOWN_BLOCK_SIZE_0 +
            len(UserData.STARCRAFT_2_MAGIC_NAME)]

        if UserData.STARCRAFT_2_MAGIC_NAME != sc2_user_data_replay:
            return False

        self.__major_version['Initial Release'], self.__major_version['Patch'] = \
            unpack('=HH', self.__user_data[0x1C:0x1C+4])
        self.__build_number = unpack('=H', self.__user_data[0x20:0x20+2])[0]

        self.__replay_file.seek(0)
        return True

    def __str__(self):
        """Provide basic information about the User Data block."""
        return_value = '''MPQ User Data:
    Archive Header Offset : {0:6} bytes
    User Data Size        : {1:6} bytes
    Initial Release       : {2:6}
    Patch                 : {3:6}
    Build Number          : {4:6}
'''.format(self.__archive_header_offset, self.__user_data_size,
           self.__major_version['Initial Release'], self.__major_version['Patch'],
           self.__build_number)
        return return_value

    def get_archive_header_offset(self):
        """Provide external access to the archive header offset.
        Read only access.
        """
        return self.__archive_header_offset

    # Read only property for the Archive Header Offset
    archive_header_offset = property(get_archive_header_offset)
