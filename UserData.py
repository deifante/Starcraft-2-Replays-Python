from struct import *

class UserData:
    """Reads the user data block of the sc2 replay file."""
    STARCRAFT_2_USER_DATA_MAGIC_VALUE = 458313805 # MPQ0x1B
    STARCRAFT_2_MAGIC_NAME            = 'StarCraft II replay'
    USER_DATA_UNKNOWN_BLOCK_SIZE_0    = 9

    def __init__(self, file_name):
        """Instantiate a User Data block reading object.
        Keword arguments:
        file_name -- the full path of the file. May be relative or absolute.
        """
        self.file_name             = file_name
        self.user_data_size        = 0
        self.archive_header_offset = 0
        self.user_data             = None

    def read(self):
        """"Verify that the User Data block is as expected."""
        replay_file = open(self.file_name, 'rb')
        data_buffer = replay_file.read(4)
        magic_value = unpack('=i', data_buffer)[0]
        print 'magic_value', magic_value
        if UserData.STARCRAFT_2_USER_DATA_MAGIC_VALUE != magic_value:
            replay_file.close()
            return False

        self.user_data_size, self.archive_header_offset = unpack('=II', replay_file.read(8))
        self.user_data = replay_file.read(self.user_data_size)

        valid_data_length = unpack('=I', self.user_data[:4])[0]
        print 'valid_data_length', valid_data_length

        sc2_user_data_replay = self.user_data[
            UserData.USER_DATA_UNKNOWN_BLOCK_SIZE_0 :
                UserData.USER_DATA_UNKNOWN_BLOCK_SIZE_0 +
            len(UserData.STARCRAFT_2_MAGIC_NAME)]
        
        if UserData.STARCRAFT_2_MAGIC_NAME != sc2_user_data_replay:
            return False

        replay_file.close()
        return True

if __name__ == "__main__":
    user_data = UserData('samples/Victory-of-the-Year.SC2Replay')
    if user_data.read():
        print 'User Data Read'
    else:
        print 'User Data Not Valid'
