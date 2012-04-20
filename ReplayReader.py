from struct import *

from ArchiveHeader import ArchiveHeader
from UserData import UserData
from BlockTable import BlockTable

class ReplayReader(object):
    """Takes responsibility for reading the entire replay.
    Also implements some general use algorithms.
    """
    def __init__(self, file_name):
        self._file_name      = file_name
        self._user_data      = None
        self._archive_header = None
        self._block_table    = None
        self._file_contents  = None
        self._crypt_table    = range(0x500)
        self.create_crypt_table()

    def read(self):
        self._file_contents = open(self._file_name, 'rb')
        self._user_data = UserData(self._file_contents)
        if not self._user_data.read():
            return False
        print self._user_data

        self._archive_header = ArchiveHeader(self._file_contents, self._user_data)
        if not self._archive_header.read():
            return False
        print self._archive_header

        self._block_table = BlockTable(self._file_contents, self._archive_header)
        self._block_table.read()
        print self._block_table

    def create_crypt_table(self):
        seed = 0x00100001

        for index1 in range(0x100):
            index2 = index1
            for i in range(5):
                seed = (seed * 125 + 3) % 0x2AAAAB
                temp1 = (seed & 0xFFFF) << 0x10

                seed = (seed * 125 + 3) % 0x2AAAAB
                temp2 = seed & 0xFFFF
                self._crypt_table[index2] = (temp1 | temp2)
                index2 += 0x100

    def decrypt(self, data_block, length, key):
        seed = 0xEEEEEEEE
        length >> 2
        data_block_index

        # while(length > 0):
        #     length -= 1
        #     seed += self._crypt_table[0x400 + (key & 0xFF)]
        #     ch = unpack('=I', data_block[data_block_index:data_block_index + 4]) ^ (key + seed)


    def hash(self, name, hash_type):
        seed1 = 0x7FED7FED
        seed2 = 0xEEEEEEEE

        for ch in name:
            ch = ord(ch.upper())
            seed1 = self._crypt_table[(hash_type << 8) + ch] ^ (seed1 + seed2) & 0xFFFFFFFF
            seed2 = ch + seed1 + seed2 + (seed2 << 5) + 3 & 0xFFFFFFFF
        return seed1

if __name__ == "__main__":
    replay_reader = ReplayReader('samples/Victory-of-the-Year.SC2Replay')
    #replay_reader = ReplayReader('samples/2v2.sc2replay')
    # replay_reader.read()
    hash_value = replay_reader.hash('arr\units.dat', 0)
    print 'hash value: Ox{0:X}\nhash value type:{1}'.format(hash_value, type(hash_value))

    print 'Done'
