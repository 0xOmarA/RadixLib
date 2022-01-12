from . import network_specific_constants as NetworkSpecificConstants
from .network import Network
from Crypto.Cipher._mode_gcm import GcmMode
from Crypto.Protocol.KDF import scrypt
from typing import List, Tuple, Dict, Union
from ecdsa.keys import SigningKey
from ecdsa.util import sigencode_der
from ecdsa.curves import SECP256k1
from hdwallet import HDWallet
from Crypto.Cipher import AES
import mnemonic
import hashlib
import bech32
import ecdsa
import json


class Signer():
    """ 
    This is a class implementation of a Signer Wallet. This Signer object is able 
    to generate the raidx address, as well as the public and private keys through 
    the following: 

    * The 12 word mnemonic phrase.
    * The `wallet.json` file.
    * The seedphrase.

    In addition to that, this wallet object is aware of the existance of multiple
    radix addresses using the `address_index` parameter.

    Many parts of this `Signer` class were made possible thanks to Stuart from
    RadixPool and his amazing article here: 
    https://docs.radixpool.com/decoding-the-radix-wallet
    """

    HD_WALLET_PARAMS: Dict[str, Tuple[int, bool]] = {
        "purpose": (44, True),
        "coinType": (1022, True),
        "account": (0, True),
        "change": (0, False),
    }

    def __init__(
        self,
        seed: bytes
    ) -> None:
        """
        A method used to create new radix signer through the mnemonic phrase

        # Arguments

        * `seed: bytes` - The seed which the wallet uses given as `bytes`.
        """

        self.__seed: bytes = seed

    @classmethod
    def new_random(cls) -> 'Signer':
        """ A method used to create a new Random signer object """
        
        return cls.from_mnemonic(mnemonic.Mnemonic('english').generate(128))

    @classmethod
    def from_mnemonic(
        cls,
        mnemonic_phrase: Union[str, List[str]]
    ) -> 'Signer':
        """
        This method is used to generate a new radix signer through the mnemonic phrase 
        of the wallet.

        # Arguments:

        * `mnemonic_phrase: Union[str, List[str]]` - A string or a list of strings of the
        mnemonic phrase for the given signer

        # Returns

        * `Signer` - A new signer object
        """

        # If the supplied mnemonic phrase is a list then convert it to a string
        if isinstance(mnemonic_phrase, list):
            mnemonic_phrase: str = " ".join(
                map(lambda x: str(x).lower(), mnemonic_phrase))

        return cls(mnemonic.Mnemonic.to_seed(mnemonic_phrase))

    @classmethod
    def from_wallet_json(
        cls,
        wallet_json_path: str,
        passphrase: str
    ) -> 'Signer':
        """ 
        This method is used to generate a new radix signer from the `wallet.json` file
        and the corresponding spending password that the wallet uses.

        # Arguments

        - `wallet_json_path: str` - A string of thw path to the `wallet.json` file which 
        comes with the radix wallet.
        - `passphrase: str` - The passphrase which the wallet uses for the spending.

        # Returns

        * `Signer` - A new signer object
        """

        # Opening and reading the wallet.json file
        with open(wallet_json_path, 'r') as file:
            wallet_json: dict = json.load(file)
            wallet_json['seed'] = json.loads(wallet_json['seed'])

        # Getting the important information from the wallet json file
        salt: str = wallet_json['seed']['crypto']['kdfparams']['salt']
        length_of_derived_key: int = wallet_json['seed']['crypto']['kdfparams']['lengthOfDerivedKey']
        cost_param_n: int = wallet_json['seed']['crypto']['kdfparams']['costParameterN']
        block_size: int = wallet_json['seed']['crypto']['kdfparams']['blockSize']
        parallelization_parameter: int = wallet_json['seed'][
            'crypto']['kdfparams']['parallelizationParameter']

        cipher_type: str = wallet_json['seed']['crypto']['cipher']
        cipher_text: str = wallet_json['seed']['crypto']['ciphertext']
        nonce: str = wallet_json['seed']['crypto']['cipherparams']['nonce']
        mac: str = wallet_json['seed']['crypto']['mac']

        # Calculating the symetrical key through the salt
        symetrical_key: bytes = scrypt(
            password=passphrase,
            salt=bytearray.fromhex(salt),
            key_len=length_of_derived_key,
            N=cost_param_n,
            r=block_size,
            p=parallelization_parameter
        )

        # Decrypting the cipher phrase into its entropy using the symetrical key
        entropy: bytes = AES.new(
            key=symetrical_key,
            mode=getattr(AES, f"MODE_{cipher_type.split('-')[-1]}"),
            nonce=bytearray.fromhex(nonce)
        ).decrypt_and_verify(
            ciphertext=bytearray.fromhex(cipher_text),
            received_mac_tag=bytearray.fromhex(mac)
        )

        # Creating the mnemonic phrase from the entropy
        mnemonic_phrase: List[str] = mnemonic.Mnemonic('english').to_mnemonic(entropy).split(' ')

        # Using the mnemonic phrase to create the final seed
        seed: bytes = mnemonic.Mnemonic('english').to_seed(" ".join(mnemonic_phrase).encode('utf-8'), "")

        return cls(seed)

    def hdwallet_object(
        self, 
        index: int = 0
    ) -> HDWallet:
        """ 
        A method used to create HDWallet object with the Radix parameters for a given address
        index.

        # Arguments:

        * `index: int` - An integer of the address_index which we wish to use for the HDWallet
        object creation

        # Returns:

        * `HDWallet` - An HD wallet object created with the Radix Parameters and with the given
        `index`
        """

        hdwallet: HDWallet = HDWallet()
        hdwallet.from_seed(seed=self.__seed.hex())
        for name, values_tuple in self.HD_WALLET_PARAMS.items():
            value, hardened = values_tuple
            hdwallet.from_index(value, hardened=hardened)
        hdwallet.from_index(index, True)

        return hdwallet

    def public_key(
        self, 
        index: int = 0
    ) -> str:
        """ 
        A method used to generate the public key corresponding to the wallet at the given
        address index.

        # Arguments:

        * `index: int` - The index of the address to use for the generation of the public 
        key

        # Returns:

        * `str` - A string of the public key for the wallet
        """

        return str(self.hdwallet_object(index).public_key())

    def private_key(
        self, 
        index: int = 0
    ) -> str:
        """ 
        A method used to generate the private key corresponding to the wallet at the given
        address index.

        # Arguments:

        * `index: int` - The index of the address to use for the generation of the private 
        key

        # Returns:

        * `str` - A string of the private key for the wallet
        """

        return str(self.hdwallet_object(index).private_key())

    def wallet_address(
        self, 
        index: int = 0, 
        mainnet: bool = True
    ) -> str:
        """ 
        A method used to generate the wallet address for this given signer at the given index

        # Arguments:

        * `index: int` - The index of the address to use for the generation of the address
        * `mainnet: bool` - A boolean of whether to use the mainnet or the stokenet

        # Returns:

        * `str` - A string of the wallet address
        """

        return bech32.bech32_encode(
            hrp = NetworkSpecificConstants.WALLET_ADDRESS_HRP[Network.MAINNET if mainnet else Network.STOKENET],
            data=bech32.convertbits(b"\x04" + bytearray.fromhex(self.hdwallet_object(index=index).public_key()), 8, 5)
        )

    def sign(
        self, 
        data: str, 
        index: int = 0
    ) -> str:
        """ 
        A method used to sign data using the private keys for the radix wallet

        # Arguments:

        * `data: str` - A string of the data which we wish to sign.
        * `index: int` - The index of the address to use for the generation of the private 
        key.

        # Returns:

        * `str` - A string of the signed data
        """

        signing_key: SigningKey = ecdsa.SigningKey.from_string(
            string=bytearray.fromhex(self.private_key(index)),
            curve=SECP256k1,
            hashfunc=hashlib.sha256
        )

        return signing_key.sign_digest(bytearray.fromhex(data), sigencode=sigencode_der).hex()