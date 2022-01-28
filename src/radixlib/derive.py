from .network import Network
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
        string = hashlib.sha256(
            string = pub_key_symbol_concat
        ).digest()
    ).digest()

    return bech32.bech32_encode(
        hrp = f"{token_symbol}{network.resource_hrp_suffix}", 
        data = bech32.convertbits( #type: ignore
            data = b"\x03" + final_hash[6:32], 
            frombits = 8 ,
            tobits = 5
        )
    )