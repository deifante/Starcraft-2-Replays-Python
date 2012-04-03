from struct import *

class BlockHeader(object):
    """Reads a Block Table from a Starcraft 2 Replay."""
    
    def __init__(self, replay_file, archive_header):
        """Instantiate a block header reading object.

        Keyword arguments:
        replay_file -- The already opened replay file.
        archive_header -- Archive Header information from the same replay file.
        """
        self.__block_offset = 0
        self.__block_size   = 0
        self.__file_size    = 0
