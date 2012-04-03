from ArchiveHeader import ArchiveHeader
from UserData import UserData
from BlockTable import BlockTable

class ReaplayReader(object):
    """Takes responsibility for reading the entire replay."""
    def __init__(self, file_name):
        self.file_name      = file_name
        self.user_data      = None
        self.archive_header = None
        self.block_table    = None
        self.file_contents  = None

    def read(self):
        self.file_contents = open(self.file_name, 'rb')
        self.user_data = UserData(self.file_contents)
        if not self.user_data.read():
            return False
        print self.user_data

        self.archive_header = ArchiveHeader(self.file_contents, self.user_data)
        if not self.archive_header.read():
            return False
        print self.archive_header

        self.block_table = BlockTable(self.file_contents, self.archive_header)
        self.block_table.read()
        print self.block_table

if __name__ == "__main__":
    replay_reader = ReaplayReader('samples/Victory-of-the-Year.SC2Replay')
    #replay_reader = ReaplayReader('samples/2v2.sc2replay')
    replay_reader.read()
    print 'Done'
