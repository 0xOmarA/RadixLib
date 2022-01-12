from . import network_specific_constants as NetworkSpecificConstants
from ecdsa.keys import SigningKey, VerifyingKey
from ecdsa.ellipticcurve import PointJacobi
from Crypto.Cipher._mode_gcm import GcmMode
from Crypto.Protocol.KDF import scrypt
from ecdsa.curves import SECP256k1
from Crypto.Cipher import AES
from .network import Network
from typing import Union
import hashlib
import bech32
import ecdsa
import os


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


def encrypt_message(
    sender_private_key: str,
    receiver_public_key: str,
    message: str,
) -> str:
    """
    This method is used to encrypt a message such that only the receiver of the message
    would be able to open the message and view its content. This is a standard practice 
    and functionality in the Radix desktop wallet.

    # Arguments

    * `sender_private_key: str` - The private key of the sender where the message originated
    * `receiver_public_key: str` - The public key of the receiver to who the message is sent
    * `message: str` - The message we wish the encrypt

    # Returns

    * `str` - A string of the encrypted message
    """
    # Creating an Ephemeral key
    ephemeral_private_key: SigningKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
    ephemeral_public_key: VerifyingKey = ephemeral_private_key.get_verifying_key()

    # Creating the shared secret of the Diffie-Hellman through the public, private, and the ephemeral key
    public_key_point: PointJacobi = VerifyingKey.from_string(bytearray.fromhex(receiver_public_key), curve=SECP256k1, hashfunc=hashlib.sha256).pubkey.point
    private_key_point: int = SigningKey.from_string(bytearray.fromhex(sender_private_key), curve=SECP256k1, hashfunc=hashlib.sha256).privkey.secret_multiplier
    ephemeral_private_key_point: PointJacobi = ephemeral_public_key.pubkey.point

    shared_secret: bytes = ((public_key_point * private_key_point) + ephemeral_private_key_point).x().to_bytes(32, 'big')

    # Creating the key through through the salt
    nonce: bytes = os.urandom(12) 
    salt: bytes = hashlib.sha256(nonce).digest()
    key: bytes = scrypt(
        password = shared_secret,
        salt = salt,
        key_len = 32,
        N = 8192,
        r = 8,
        p = 1
    )

    # Creating a new cipher and adding the ephemeral key to it
    cipher: GcmMode = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(ephemeral_public_key.to_string("compressed"))

    # Encrypt the message
    ciphertext: bytes
    auth_tag: bytes
    ciphertext, auth_tag = cipher.encrypt_and_digest(message.encode())

    # Getting the final representation of the message after the message
    # encryption
    return (bytearray(b'\x01') + bytearray(b'\xff') + bytearray(ephemeral_public_key.to_string("compressed")) + bytearray(nonce) + bytearray(auth_tag) + bytearray(ciphertext)).hex()