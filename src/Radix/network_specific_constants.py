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

XRD: Dict[Network, str] = {
    Network.MAINNET: "xrd_rr1qy5wfsfh",
    Network.STOKENET: "xrd_tr1qyf0x76s"
}
""" A dictionary mapping of the network type and the RRI of the XRD tokens accross the Mainnet and the Stokenet """

TOKEN_HRP: Dict[Network, str] = {
    Network.MAINNET: "rr",
    Network.STOKENET: "tr"
}
""" A dictionary mapping of the network type and the HRP used for new tokens created on that specific network """