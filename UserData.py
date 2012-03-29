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

        valid_data_length = unpack('=I', self.__user_data[:4])[0]

        sc2_user_data_replay = self.__user_data[
            UserData.USER_DATA_UNKNOWN_BLOCK_SIZE_0:
                UserData.USER_DATA_UNKNOWN_BLOCK_SIZE_0 +
            len(UserData.STARCRAFT_2_MAGIC_NAME)]

        if UserData.STARCRAFT_2_MAGIC_NAME != sc2_user_data_replay:
            return False

        self.__replay_file.seek(0)
        return True

    def __str__(self):
        """Provide basic information about the User Data block."""
        return_value = '''MPQ User Data:
    Archive Header Offset: %u bytes
    User Data Size       : %u bytes''' % \
        (self.__archive_header_offset, self.__user_data_size)
        return return_value

    def get_archive_header_offset(self):
        """Provide external access to the archive header offset.
        Read only access.
        """
        return self.__archive_header_offset

    archive_header_offset = property(get_archive_header_offset)
