from dataclasses import dataclass
from typing import Optional

@dataclass(frozen = True)
class Network():
    """ Describes a network for the Radix blockchain and the HRP needed for derivations of addresses

    Aside from the mainnet, there are a number of other networks which run the RadixDLT software. 
    These networks are usually used for development and to test new features. These networks have 
    different names and different HRPs; thus, the derivation of wallet addresses, node addresses,
    and token RRIs is different. This network class defines a network along with its name and the
    needed HRPs for the derivations needed.

    You may use this network class to define your own custom networks such that other functions and
    classes in this library can use your custom defined network.

    Args:
        name (str): The name of the network
        account_hrp (str): The HRP used for the derivation of the wallet addresses
        resource_hrp_suffix (str): The postfix added to the HRP when deriving the RRI of resources
        node_hrp (str): The HRP used for the derivation of node addresses
        validator_hrp (str): The HRP used for the derivation of validator addresses
        default_gateway_url (:obj:`str`, optional): The URL for a default gateway API to connect to
            when on this network.
    """
    name: str
    account_hrp: str
    resource_hrp_suffix: str
    node_hrp: str
    validator_hrp: str
    default_gateway_url: Optional[str] = None
 
MAINNET: Network = Network(
    name = "mainnet",
    account_hrp = "rdx",
    resource_hrp_suffix = "_rr",
    node_hrp = "rn",
    validator_hrp = "rv",
    default_gateway_url = "https://mainnet.radixdlt.com"
)
""" Describes the information of the mainnet and its HRPs """

STOKENET: Network = Network(
    name = "stokenet",
    account_hrp = "tdx",
    resource_hrp_suffix = "_tr",
    node_hrp = "tn",
    validator_hrp = "tv",
    default_gateway_url = "https://stokenet.radixdlt.com"
)
""" Describes the information of the stokenet and its HRPs """

BETANET: Network = Network(
    name = "betanet",
    account_hrp = "bdx",
    resource_hrp_suffix = "_br",
    node_hrp = "bn",
    validator_hrp = "bv",
    default_gateway_url = "https://betanet.radixdlt.com"
)
""" Describes the information of the stokenet and its HRPs """