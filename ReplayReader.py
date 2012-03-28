from ArchiveHeader import ArchiveHeader
from UserData import UserData

class ReaplayReader(object):
    """Takes responsibility for reading the entire replay."""
    def __init__(self, file_name):
        self.file_name      = file_name
        self.user_data      = None
        self.archive_header = None
        self.file_contents  = None

    def read(self):
        self.file_contents = open(self.file_name, 'rb')
        self.user_data = UserData(self.file_contents)
        if not self.user_data.read():
            return False
        print self.user_data        
        self.archive_header = ArchiveHeader(self.file_contents, self.user_data.archive_header_offset)
        self.archive_header.read()
        print self.archive_header

if __name__ == "__main__":
    replay_reader = ReaplayReader('samples/Victory-of-the-Year.SC2Replay')
    replay_reader.read()
    print 'Done'
    # user_data = UserData('samples/Victory-of-the-Year.SC2Replay')
    # user_data.read()
    # header = ArchiveHeader('samples/Victory-of-the-Year.SC2Replay')
    # if header.verify_file():
    #     print 'Valid File'
    #     header.read()
