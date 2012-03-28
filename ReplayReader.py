from ArchiveHeader import ArchiveHeader
from UserData import UserData

class ReaplayReader:
    """Takes responsibility for reading the entire replay."""
    def __init__(self, file_name):
        self.user_data = None
        self.archive_header = None

    def read(self):
        replay_file = open(self.file_name, 'rb')

if __name__ == "__main__":
    replay_reader = ReaplayReader('samples/Victory-of-the-Year.SC2Replay')
    print 'Done'
    # user_data = UserData('samples/Victory-of-the-Year.SC2Replay')
    # user_data.read()
    # header = ArchiveHeader('samples/Victory-of-the-Year.SC2Replay')
    # if header.verify_file():
    #     print 'Valid File'
    #     header.read()
