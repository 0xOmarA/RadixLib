from typing import Optional, Dict, Any, TypeVar, Union, List, Tuple, Set, BinaryIO, overload
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
import io

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

__T = TypeVar('__T', Dict[Any, Any], List[Any], Tuple[Any], Set[Any])
def convert_to_dict_recursively(
    iterable: __T
) -> __T:
    """ Converts the individual items in an iterable to a dictionary if they're an instance of the
    Serializable class.

    This function recursively checks for Serializable objects in the iterable passed to it and 
    invokes the `to_dict` method on all of the objects that if finds which are Serializable. This 
    function is executed on the objects which have been converted to a dictionary to ensure that 
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
    """ Encrypts a message using the new format used by the Radix Olympia wallet.
    
    This method is used to encrypt a message such that only the receiver of the message
    would be able to open the message and view its content. This is a standard practice 
    and functionality in the Radix desktop wallet.
    
    Args:
        sender_private_key (str): The private key of the sender where the message originated
        receiver_public_key (str): The public key of the receiver to who the message is sent
        message (str): The message we wish the encrypt
    
    Returns
        str: A string of the encrypted message
    """
    # Creating an Ephemeral key
    ephemeral_private_key: SigningKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256) # type: ignore
    ephemeral_public_key: VerifyingKey = ephemeral_private_key.get_verifying_key() # type: ignore

    # Creating the shared secret of the Diffie-Hellman through the public, private, and the ephemeral key
    public_key_point: PointJacobi = VerifyingKey.from_string(bytearray.fromhex(receiver_public_key), curve=SECP256k1, hashfunc=hashlib.sha256).pubkey.point # type: ignore
    private_key_point: int = SigningKey.from_string(bytearray.fromhex(sender_private_key), curve=SECP256k1, hashfunc=hashlib.sha256).privkey.secret_multiplier # type: ignore
    ephemeral_public_key_point: PointJacobi = ephemeral_public_key.pubkey.point # type: ignore

    shared_secret: bytes = ((public_key_point * private_key_point) + ephemeral_public_key_point).x().to_bytes(32, 'big') # type: ignore

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

@overload
def decode_message(message_bytes: str) -> str: ...

@overload
def decode_message(message_bytes: str, public_key: str, private_key: str) -> str: ...

def decode_message(
    message_bytes: str,
    public_key: Optional[str] = None,
    private_key: Optional[str] = None,
) -> str:
    """ Decodes the message bytes into a utf-8 encoded string.

    Args:
        message_bytes (str): A string of the message bytes in hex.
        public_key (str, optional): An optional argument passed only when the message is 
            believed to be encrypted. If passed when the message is not encrypted then it wont be 
            used for any operations.
        private_key (str, optional): An optional argument passed only when the message is 
            believed to be encrypted. If passed when the message is not encrypted then it wont be 
            used for any operations.
    
    Returns:
        str: A string of the decoded message
    """

    # Converting the message into a binary IO to make the reading of the data easier 
    message_io: BinaryIO = io.BytesIO(bytearray.fromhex(message_bytes))

    # Loading the data packed in the message bytes
    message_type: int = message_io.read(1)[0]
    encryption_type: bytes = message_io.read(1)

    if message_type == 0x0: # In this case the message is not encrypted, just encoded in UTF-8
        return message_io.read().decode('utf-8')
    
    elif message_type == 0x1: # In this case the message is encrypted and encoded in UTF-8
        if encryption_type[0] != 0xFF:
            raise NotImplementedError("This function only supports the decryption of 0xFF type encryption (AES-GCM)")

        # Ensure that in the case that the message is encrypted that both the public and private keys
        # are provided
        if public_key is None or private_key is None:
            raise ValueError("This message appears to be encrypted and you need to provide the public and private keys for encrypted messages.")

        # Loading up the remaining information in the encrypted message
        ephemeral_public_key: bytes = message_io.read(33)
        nonce: bytes = message_io.read(12)
        auth_tag: bytes = message_io.read(16)
        cipher_text: bytes = message_io.read()

        # Creating the shared secret of the Diffie-Hellman through the public, private, and the ephemeral key
        public_key_point: PointJacobi = VerifyingKey.from_string(bytearray.fromhex(public_key), curve=SECP256k1, hashfunc=hashlib.sha256).pubkey.point # type: ignore
        private_key_point: int = SigningKey.from_string(bytearray.fromhex(private_key), curve=SECP256k1, hashfunc=hashlib.sha256).privkey.secret_multiplier # type: ignore
        ephemeral_public_key_point: PointJacobi = VerifyingKey.from_string(string = ephemeral_public_key, curve = SECP256k1, hashfunc=hashlib.sha256).pubkey.point # type: ignore

        shared_secret: bytes = ((public_key_point * private_key_point) + ephemeral_public_key_point).x().to_bytes(32, 'big') # type: ignore

        # Creating the key through the information in the message
        salt: bytes = hashlib.sha256(bytearray(nonce)).digest()
        key: bytes = scrypt( # type: ignore
            password = bytearray(shared_secret), # type: ignore
            salt = salt, # type: ignore
            key_len = 32,
            N = 8192,
            r = 8,
            p = 1
        )

        # Creating a new cipher and adding the ephemeral key to it
        cipher: GcmMode = AES.new(key, AES.MODE_GCM, nonce=nonce) # type: ignore
        cipher.update(ephemeral_public_key) # type: ignore

        # Decrypting the data and returning it
        plain_text: bytes = cipher.decrypt_and_verify(cipher_text, auth_tag)
        return plain_text.decode('utf-8')

    elif message_type == 0x30: # In this case the message follows the legacy double encoded format
        # When the message has the double encoded format then all that we need to do is pass the 
        # decoded format back to the function again so that it can perform the decoding accordingly.
        return decode_message(
            message_bytes = bytearray.fromhex(message_bytes).decode('utf-8'),
            public_key = public_key,                    # type: ignore 
            private_key = private_key                   # type: ignore
        )
    
    else:
        raise NotImplementedError("No decoding programmed for the provided message type")