from enum import Enum

class NetworkType(Enum):
    MAINNET = 'mainnet'
    STOKENET = 'stokenet'

    def __str__(self) -> str:
        """ Represents the network type as a string """
        return self.value