from radixlib.network import Network
import hashlib
import bech32


def wallet_address_from_public_key(
    public_key: str,
    network: Network
) -> str:
    """ Derives the wallet address on the specified network for the given public key. 
    
    Args: 
        public_key (str): The public key to use for the wallet address derivation
        network (Network): The network that the address is being derived for.

    Returns:
        str: A string of the wallet address
    """

    return bech32.bech32_encode(
        hrp = network.account_hrp,
        data = bech32.convertbits(
            data = b"\x04" + bytearray.fromhex(public_key), 
            frombits = 8, 
            tobits = 5
        ) #type: ignore
    )

def public_key_from_wallet_address(wallet_address: str) -> str:
    """ Derives the public key of a wallet from the wallet address.
    
    Args:
        wallet_address (str): The wallet address to use for the public key derivation

    Returns:
        str: A string of the public key
    """

    return bytes(bech32.convertbits(
        data = bech32.bech32_decode(wallet_address)[1], #type: ignore
        frombits = 5,
        tobits = 8,
        pad = False
    )[1:34]).hex()

def public_key_from_node_or_validator_address(node_or_validator_address: str) -> str:
    """ Derives the public key for a given node or validator through their addresses.
    
    Args:
        node_or_validator_address (str): The address of the node or the validator

    Returns:
        str: A string of the public key
    """

    return bytes(bech32.convertbits(
        data = bech32.bech32_decode(node_or_validator_address)[1], #type: ignore
        frombits = 5,
        tobits = 8,
        pad = False
    )).hex()

def wallet_address_on_other_network(
    wallet_address: str,
    network: Network
) -> str:
    """ Converts the wallet address from whatever network it currently uses to another network.
    
    This method converts the given wallet address to its equivalent public key first then derives 
    the address on the new network from the public key.

    Args:
        wallet_address (str): The wallet address that we want to convert to another network
        network (Network): The destination network

    Returns:
        str: The wallet address on the specified network
    """

    return wallet_address_from_public_key(
        public_key = public_key_from_wallet_address(wallet_address),
        network = network
    )

def token_rri(
    creator_public_key: str,
    token_symbol: str,
    network: Network
) -> str:
    """ Derives the token RRI on a given network from the token symbol and public key of creator.

    Args:
        creator_public_key (str): The public key of the creator of the token
        token_symbol (str): The symbol of the token (typically 3 to 8 characters)
        network (Network): The network that the token was created on
    
    Returns:
        str: A string of the token RRI.
    """

    # In the calculation of the RRI, we need the token symbol to always be small case.
    token_symbol = token_symbol.lower()

    # Concatenating the public key and the token symbol to get the string that we need
    # to hash
    pub_key_symbol_concat: bytearray = bytearray.fromhex(creator_public_key) + token_symbol.encode()

    final_hash: bytes = hashlib.sha256(
        hashlib.sha256(pub_key_symbol_concat).digest()
    ).digest()

    return bech32.bech32_encode(
        hrp = f"{token_symbol}{network.resource_hrp_suffix}", 
        data = bech32.convertbits( #type: ignore
            data = b"\x03" + final_hash[6:32], 
            frombits = 8 ,
            tobits = 5
        )
    )

def node_address_from_public_key(
    public_key: str,
    network: Network
) -> str:
    """ Derives the node address from the public key given.
    
    Args:
        public_key (str): The public key to use for the node address derivation.
        network (Network): The network that the address is being derived for.

    Returns:
        str: The node address
    """

    return bech32.bech32_encode(
        hrp = network.node_hrp,
        data = bech32.convertbits(
            data = bytearray.fromhex(public_key), 
            frombits = 8, 
            tobits = 5
        ) #type: ignore
    )

def validator_address_from_public_key(
    public_key: str,
    network: Network
) -> str:
    """ Derives the validator address from the public key given.
    
    Args:
        public_key (str): The public key to use for the validator address derivation.
        network (Network): The network that the address is being derived for.

    Returns:
        str: The validator address
    """

    return bech32.bech32_encode(
        hrp = network.validator_hrp,
        data = bech32.convertbits(
            data = bytearray.fromhex(public_key), 
            frombits = 8, 
            tobits = 5
        ) #type: ignore
    )

def xrd_rri_on_network(network: Network):
    """ Derives the RRI of the native token (XRD) on the given network.
    
    Args:
        network (Network): The network to derive the XRD RRI for.

    Returns:
        str: A string of the XRD RRI on that network.
    """

    # To derive the RRI of XRD on another network, we need to use it's RRI on a known network first
    # to get the data from the bech32 encoded RRI. So, the operation that we're esentially doing is
    # just re-encoding the data with a different HRP.
    known_rri: str = "xrd_rr1qy5wfsfh"

    return bech32.bech32_encode(
        hrp = f"xrd{network.resource_hrp_suffix}",
        data = bytearray(bech32.bech32_decode(known_rri)[1]) # type: ignore
    )

def xrd_from_atto(atto_amount: int) -> float:
    """ Converts an amount of Atto to their XRD equivalent
    
    Args:
        atto_amount (int): The amount of atto to get in XRD.

    Returns:
        float: The equivalent amount of XRD.
    """

    return atto_amount / (10**18)

def atto_from_xrd(xrd_amount: float) -> int:
    """ Converts an amount of XRD to their Atto equivalent
    
    Args:
        xrd_amount (int): The amount of XRD to get in Atto.

    Returns:
        float: The equivalent amount of Atto.
    """

    return int(xrd_amount * 10**18)