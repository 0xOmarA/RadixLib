from typing import Dict, Any, Union, List, Tuple, Set
from radixlib.serializable import Serializable

from ecdsa.keys import SigningKey, VerifyingKey
from ecdsa.ellipticcurve import PointJacobi
from Crypto.Cipher._mode_gcm import GcmMode
from Crypto.Protocol.KDF import scrypt
from ecdsa.curves import SECP256k1
from Crypto.Cipher import AES
import hashlib
import ecdsa
import os

def remove_none_values_recursively(dictionary: Dict[Any, Any]) -> Dict[Any, Any]:
    """ Recursively removes the key value pairs where the value is None. 

    This is a recursive function which tries to find key value pairs where the value is None and 
    then remove these pairs from the dictionary. 

    Args:
        dictionary (dict): The dictionary to remove the None values from.

    Returns:
        dict: A dictionary with the None value pairs removed.
    """

    return {
        key: remove_none_values_recursively(value) if isinstance(value, dict) else value # type: ignore
        for key, value in dictionary.items()
        if value is not None
    }

def convert_to_dict_recursively(
    iterable: Union[Dict[Any, Any], List[Any], Tuple[Any], Set[Any]]
) -> Union[Dict[Any, Any], List[Any], Tuple[Any], Set[Any]]:
    """ Converts the individual items in an iterable to a dictionary if they're an instance of the
    Serializable class.

    This function recursively checks for Serializable objects in the iterable passed to it and 
    invokes the `to_dict` method on all of the objects that if finds which are Serializable. This 
    function is excuted on the objects which have been converted to a dictionary to ensure that 
    the entire dictionary is in a valid format.

    Args:
        iterable (Union[Dict[Any, Any], List[Any], Tuple[Any], Set[Any]]): An iterable which could 
            be a dictionary, list, tuple, or set to convert all of its Serializable objects into 
            their dictionary form.

    Returns:
        Union[Dict[Any, Any], List[Any], Tuple[Any], Set[Any]]: The iterable object reconstructed
            with all of the Serializable objects converted into a dictionary.
    
    """
    if isinstance(iterable, dict):
        new_dict: Dict[Any, Any] = {}
    
        for key, value in iterable.items():
            if isinstance(value, Serializable):
                new_dict[key] = convert_to_dict_recursively(value.to_dict())
            elif isinstance(value, (dict, list, tuple, set)):
                new_dict[key] = convert_to_dict_recursively(value) # type: ignore
            else:
                new_dict[key] = value

        return new_dict
    
    elif isinstance(iterable, (list, tuple, set)): # type: ignore
        new_list: List[Any] = []

        for item in iterable:
            if isinstance(item, Serializable):
                new_list.append(convert_to_dict_recursively(item.to_dict()))
            elif isinstance(item, (dict, list, tuple, set)):
                new_list.append(convert_to_dict_recursively(item)) # type: ignore
            else:
                new_list.append(item)

        return type(iterable)(new_list)
        
    else:
        raise NotImplementedError(
            f"No implementation for convert_to_dict_recursively available for: {type(iterable)}."
        )

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
    ephemeral_private_key: SigningKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256) # type: ignore
    ephemeral_public_key: VerifyingKey = ephemeral_private_key.get_verifying_key() # type: ignore

    # Creating the shared secret of the Diffie-Hellman through the public, private, and the ephemeral key
    public_key_point: PointJacobi = VerifyingKey.from_string(bytearray.fromhex(receiver_public_key), curve=SECP256k1, hashfunc=hashlib.sha256).pubkey.point # type: ignore
    private_key_point: int = SigningKey.from_string(bytearray.fromhex(sender_private_key), curve=SECP256k1, hashfunc=hashlib.sha256).privkey.secret_multiplier # type: ignore
    ephemeral_private_key_point: PointJacobi = ephemeral_public_key.pubkey.point # type: ignore

    shared_secret: bytes = ((public_key_point * private_key_point) + ephemeral_private_key_point).x().to_bytes(32, 'big') # type: ignore

    # Creating the key through through the salt
    nonce: bytes = os.urandom(12) 
    salt: bytes = hashlib.sha256(nonce).digest()
    key: bytes = scrypt( # type: ignore
        password = shared_secret, # type: ignore
        salt = salt, # type: ignore
        key_len = 32,
        N = 8192,
        r = 8,
        p = 1
    )

    # Creating a new cipher and adding the ephemeral key to it
    cipher: GcmMode = AES.new(key, AES.MODE_GCM, nonce=nonce) # type: ignore
    cipher.update(ephemeral_public_key.to_string("compressed")) # type: ignore

    # Encrypt the message
    ciphertext: bytes
    auth_tag: bytes
    ciphertext, auth_tag = cipher.encrypt_and_digest(message.encode())

    # Getting the final representation of the message after the message
    # encryption
    return (
        bytearray(ephemeral_public_key.to_string("compressed")) + # type: ignore
        bytearray(nonce) + 
        bytearray(auth_tag) + 
        bytearray(ciphertext)
    ).hex()