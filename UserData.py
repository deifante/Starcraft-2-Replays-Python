import struct
from collections import namedtuple

class UserData(object):
    """Reads the user data block of the MPQ file."""
    UserDataTuple = namedtuple('UserDataTuple', 'user_data_size archive_header_offset user_data')
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
        self._replay_file = replay_file
        self._user_data   = None

    def read(self):
        """"Verify that the User Data block is as expected.
        Replace the "read head" on the input file to the start of the file.
        """
        if UserData.STARCRAFT_2_USER_DATA_MAGIC_VALUE != struct.unpack('=I', self._replay_file.read(4))[0]:
            return False

        data_size, archive_header_offset = struct.unpack('=2I', self._replay_file.read(8))
        user_data = self._replay_file.read(data_size)

        sc2_user_data_replay = user_data[
            UserData.USER_DATA_UNKNOWN_BLOCK_SIZE_0:
                UserData.USER_DATA_UNKNOWN_BLOCK_SIZE_0 +
            len(UserData.STARCRAFT_2_MAGIC_NAME)]

        if UserData.STARCRAFT_2_MAGIC_NAME != sc2_user_data_replay:
            return False

        self._user_data = UserData.UserDataTuple(data_size, archive_header_offset, user_data)
        self._replay_file.seek(0)
        return True

    def __str__(self):
        """Provide basic information about the User Data block."""
        return_value = '''MPQ User Data:
    Archive Header Offset : {0:6} bytes
    User Data Size        : {1:6} bytes
'''.format(self._user_data.archive_header_offset, self._user_data.user_data_size)
        return return_value

    def get_archive_header_offset(self):
        """Provide external access to the archive header offset.
        Read only access.
        """
        return self._user_data.archive_header_offset

    # Read only property for the Archive Header Offset
    archive_header_offset = property(get_archive_header_offset)
