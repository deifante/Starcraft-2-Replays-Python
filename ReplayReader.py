from ArchiveHeader import ArchiveHeader
from UserData import UserData

if __name__ == "__main__":
    user_data = UserData('samples/Victory-of-the-Year.SC2Replay')
    user_data.read()
    # header = ArchiveHeader('samples/Victory-of-the-Year.SC2Replay')
    # if header.verify_file():
    #     print 'Valid File'
    #     header.read()
