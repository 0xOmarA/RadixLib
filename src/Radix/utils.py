from . import network_specific_constants as NetworkSpecificConstants
from ecdsa.keys import SigningKey, VerifyingKey
from ecdsa.curves import SECP256k1
from .network import Network
from typing import Union
import hashlib
import bech32


def xrd_to_atto(xrd_amount: Union[int, float, str]) -> int:
    """
    A method used to convert the supplied amount of XRD into the smallest unit
    of an XRD (called an Atto in Radix).

    # Arguments

    * `xrd_amount: xrd_amount: Union[int, float, str]` - An amount of XRD as a integer,
    float, or a string.

    # Returns

    * `int` - An integer of the amount of Atto corresponding to the XRD amount given.
    """

    return int(float(xrd_amount) * 10 ** 18)


def atto_to_xrd(atto_amount: Union[str, int]) -> float:
    """
    A method used to convert the smallest unit of an XRD (An Atto) into its equivalent
    value in XRD.

    # Arguments

    * `atto_amount: Union[str, int]` - An amount of Atto as an integer or a string. 

    # Returns

    `float` - A float of the amount of XRD corresponding to the Atto amount given.
    """

    return int(atto_amount) / (10 ** 18)


def calculate_token_rri(
    creator_public_key: str,
    token_symbol: str,
    network: Network
) -> str:
    """
    A method which is used to calculate the RRI for a new token based on the public
    key of the creator, token symbol, and the network which the token was created on.

    # Arguments

    * `creator_public_key: str` - A string of the public key of the creator of the token.
    * `token_symbol: str` - The symbol of the new token.
    * `network: Network` - The network that the token was created on. 

    # Returns

    * `str` - A string of the RRI for the token.
    """

    # All of the calculated RRIs require that the token symbol given is given
    # in small letters
    token_symbol: str = token_symbol.lower()

    final_hash: bytes = hashlib.sha256(
        string = hashlib.sha256(
            string = bytearray.fromhex(creator_public_key) + token_symbol.encode()
        ).digest()
    ).digest()

    return bech32.bech32_encode(f"{token_symbol}_{NetworkSpecificConstants.TOKEN_HRP[network]}", bech32.convertbits(b"\x03" + final_hash[6:32], 8 ,5))


def wallet_address_to_public_key(wallet_address: str) -> str:
    """
    This method is used to get the public key of any wallet by translating the wallet
    address to the corresponding public key of the wallet.

    # Arguments

    * `wallet_address: str` - A string of the wallet address that we want the public 
    key for.

    # Returns

    * `str` - A string of the public key
    """

    return bytes(bech32.convertbits(
        data = bech32.bech32_decode(wallet_address)[1],
        frombits = 5,
        tobits = 8,
        pad = False
    )[1:34]).hex()
