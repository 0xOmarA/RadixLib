"""
This file contains a number of constants on the type of network being used.
"""

from .network import Network
from typing import Dict

WALLET_ADDRESS_HRP: Dict[Network, str] = {
    Network.MAINNET: "rdx",
    Network.STOKENET: "tdx"
}
""" A dictionary which maps the network type to the hrp that should be used when generating the wallet address """