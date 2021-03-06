from typing import List, Tuple, Dict, Union, Any
from Crypto.Cipher._mode_gcm import GcmMode
from Crypto.Protocol.KDF import scrypt
from hdwallet.hdwallet import HDWallet
from ecdsa.util import sigencode_der
from ecdsa.curves import SECP256k1
from ecdsa.keys import SigningKey
from Crypto.Cipher import AES
import radixlib as radix
import mnemonic
import hashlib
import ecdsa
import json
import jwt


class Signer():
    """ A class based implementation of a signer on the Radix blockchain. The main job of the signer 
    is to derive the public and private keys from the seed phrase. 

    A signer object may be initalized using one of the following methods (using the appropriate 
    functions of course):

    #. from a `wallet.json` file generated by a Radix wallet.
    #. from the mnemonic_phrase
    #. from the seed phrase

    When a signer object is created, you may use it to sign transaction or data using the private 
    keys of the wallet.

    Many parts of this Signer class were made possible thanks to Stuart from RadixPool and his 
    article here: https://docs.radixpool.com/decoding-the-radix-wallet
    """

    HD_WALLET_PARAMS: Dict[str, Tuple[int, bool]] = {
        "purpose": (44, True),
        "coinType": (1022, True),
        "account": (0, True),
        "change": (0, False),
    }

    def __init__(
        self,
        seed: Union[bytes, bytearray, str]
    ) -> None:
        """ Instantiates a new signer object from the seed phrase
        
        Args:
            seed (Union[bytes, bytearray, str]): The seed phrase used to generate the public and 
                private keys.
        """

        self.seed: Union[bytes, bytearray] = seed if isinstance(seed, (bytes, bytearray)) else bytearray.fromhex(seed)

    @classmethod
    def new_random(cls) -> 'Signer':
        """ Creates a new signer object from a random mnemonic phrase """
        
        return cls.from_mnemonic(mnemonic.Mnemonic('english').generate(128))

    @classmethod
    def from_mnemonic(
        cls,
        mnemonic_phrase: Union[str, List[str], Tuple[str]]
    ) -> 'Signer':
        """ Instantiates a new Signer object from the mnemonic phrase passed.
        
        Args:
            mnemonic_phrase (Union[str, :obj:`list` of :obj:`str`, :obj:`tuple` of :obj:`str`): 
                A string, list, or a tuple of the mnemonic phrase. If the argument is passed as an 
                iterable, then it will be joined with a space.

        Returns:
            Signer: A new signer initalized through the mnemonic phrase.
        """

        # If the supplied mnemonic phrase is a list then convert it to a string
        if isinstance(mnemonic_phrase, (list, tuple)):
            mnemonic_string: str = " ".join(mnemonic_phrase)
        else:
            mnemonic_string: str = mnemonic_phrase

        mnemonic_string: str = " ".join(mnemonic_phrase) if isinstance(mnemonic_phrase, 
            (list, tuple)) else mnemonic_phrase

        return cls(mnemonic.Mnemonic.to_seed(mnemonic_string))

    @classmethod
    def from_encrypted_entropy(
        cls,
        encrypted_entropy_dict: Dict[str, Any],
        passphrase: str
    ) -> 'Signer':
        """ Instantiates a new Signer object from the encrypted entropy phrase typically found in the
        Olympia wallet `wallet.json` file.

        Args:
            encrypted_entropy_dict (Dict[str, Any]): The encrypted entropy.
            passphrase (str): The passphrase used by the Radix wallet to encrypt the content of the
                `wallet.json` file.

        Returns:
            Signer: A new signer initalized through the encrypted entropy.
        """

        # Getting the important information from the file
        wallet_entropy: Dict[Any, Any] = encrypted_entropy_dict['crypto']

        salt: str = wallet_entropy['kdfparams']['salt']
        length_of_derived_key: int = wallet_entropy['kdfparams']['lengthOfDerivedKey']
        cost_param_n: int = wallet_entropy['kdfparams']['costParameterN']
        block_size: int = wallet_entropy['kdfparams']['blockSize']
        parallelization_parameter: int = wallet_entropy['kdfparams']['parallelizationParameter']

        cipher_type: str = wallet_entropy['cipher']
        cipher_text: str = wallet_entropy['ciphertext']
        nonce: str = wallet_entropy['cipherparams']['nonce']
        mac: str = wallet_entropy['mac']

        # Calculating the symmetrical key through the salt
        symmetrical_key: bytes = scrypt( # type: ignore
            password = passphrase,
            salt = bytearray.fromhex(salt), # type: ignore
            key_len = length_of_derived_key,
            N = cost_param_n,
            r = block_size,
            p = parallelization_parameter
        )

        # Decrypting the cipher phrase into its entropy using the symmetrical key
        entropy: bytes = AES.new(       #type: ignore
            key = symmetrical_key,       #type: ignore
            mode = getattr(AES, f"MODE_{cipher_type.split('-')[-1]}"),
            nonce = bytearray.fromhex(nonce)
        ).decrypt_and_verify(           #type: ignore
            ciphertext=bytearray.fromhex(cipher_text),
            received_mac_tag=bytearray.fromhex(mac)
        )

        # Creating the mnemonic phrase from the entropy and then using it to create the seed phrase
        # for the signer.
        mnemonic_phrase: str = mnemonic.Mnemonic('english').to_mnemonic(entropy)
        seed: bytes = mnemonic.Mnemonic('english').to_seed(mnemonic_phrase)

        return cls(seed)

    @classmethod
    def from_wallet_json(
        cls,
        wallet_json_path: str,
        passphrase: str
    ) -> 'Signer':
        """ Instantiates a new Signer object from the `wallet.json` file created by the Radix 
        desktop wallet.

        Args:
            wallet_json_path (str): The path to the `wallet.json` file.
            passphrase (str): The passphrase used by the Radix wallet to encrypt the content of the
                `wallet.json` file.

        Returns:
            Signer: A new signer initalized through the `wallet.json` file.
        """

        # Opening and reading the wallet.json file
        with open(wallet_json_path, 'r') as file:
            wallet_json: Dict[Any, Any] = json.load(file)
            wallet_json['seed'] = json.loads(wallet_json['seed'])

        return cls.from_encrypted_entropy(wallet_json['seed'], passphrase)

    def hdwallet(
        self, 
        index: int = 0
    ) -> HDWallet:
        """ Creates an HDWallet object suitable for the Radix blockchain with the passed account 
        index.
        
        Args:
            index (int): The account index to create the HDWallet object for.
        
        Returns:
            HDWallet: An HD wallet object created with the Radix Parameters for a given account 
                index.
        """

        hdwallet: HDWallet = HDWallet()
        hdwallet.from_seed(seed=self.seed.hex())
        for _, values_tuple in self.HD_WALLET_PARAMS.items():
            value, hardened = values_tuple
            hdwallet.from_index(value, hardened=hardened)
        hdwallet.from_index(index, True)

        return hdwallet

    def public_key(
        self, 
        index: int = 0
    ) -> str:
        """ 
        Gets the public key for the signer for the specified account index
        
        Args:
            index (int): The account index to get the public keys for.

        Returns:
            str: A string of the public key for the wallet
        """

        return str(self.hdwallet(index).public_key())

    def private_key(
        self, 
        index: int = 0
    ) -> str:
        """ 
        Gets the private key for the signer for the specified account index
        
        Args:
            index (int): The account index to get the private keys for.

        Returns:
            str: A string of the private key for the wallet
        """

        return str(self.hdwallet(index).private_key())

    @property
    def master_private_key(self) -> str:
        """ Gets the master private key for the given signer
        
        Returns:
            str: A string of the master private key.
        """

        return str(self.hdwallet(0).root_xprivate_key())

    @property
    def master_public_key(self) -> str:
        """ Gets the master public key for the given signer
        
        Returns:
            str: A string of the master public key.
        """

        return str(self.hdwallet(0).root_xpublic_key())

    def sign(
        self, 
        data: str, 
        index: int = 0
    ) -> str:
        """ 
        Signs the given data using the private keys for the account at the specified account index.
        
        Arguments:
            data (str): A string of the data which we wish to sign.
            index (int): The account index to get the private keys for.
        
        Returns:
            str: A string of the signed data
        """

        signing_key: SigningKey = ecdsa.SigningKey.from_string( #type: ignore
            string=bytearray.fromhex(self.private_key(index)),
            curve=SECP256k1,
            hashfunc=hashlib.sha256
        )

        return signing_key.sign_digest( #type: ignore
            digest = bytearray.fromhex(data), 
            sigencode=sigencode_der
        ).hex() 

    def wallet_address(
        self,
        network: radix.network.Network = radix.network.MAINNET,
        index: int = 0
    ) -> str:
        """ Derives the wallet address asociated with this signer object.

        By default, the signer is supposed to be network agnostic, meaning that there should be 
        nothing in the signer that is dependent on which network we're connecting to. While this
        method goes against that and introduces network dependent elements into the design, it 
        provides an easier way of getting the wallet address for a given signer instead of having
        to call the derive module for it.
        
        Args:
            network (Network): The network to get the address for. Defaults to the mainnet when no
                argument is supplied.
            index (int): The index of the address to derive the wallet address for. Defaults to 
                address index 0 when no argument is supplied.

        Returns:
            str: A string of the wallet address.
        """

        return radix.derive.wallet_address_from_public_key(
            public_key = self.public_key(index),
            network = network
        )

    def create_jwt(
        self,
        payload: Dict[Any, Any],
        index: int = 0,
        add_public_key: bool = True
    ) -> str:
        """ Creates a JSON Web Token (JWT) signed by this signer.

        This method is used to generate JWTs that utilize the ES256K (secp256k1) algorithm which are
        signed by the private key of the account and can be verified by the account's public key. 
        The account's public key will always be provided in the payload in order to provide an easy
        way to verify the origin of the JWT.

        Args:
            payload (dict): A dictionary of the payload to include in the message.
            index (int): The index of the account to use. Defaults to zero. 
            add_public_key (bool): When this boolean is true, the public key is added to the JWT as
                a key in the body of the token. 

        Returns:
            str: A string of the created JSON Web Token (JWT)
        """

        # The methods that we will be using require that the private key is used in the PEM format.
        # so, we load the private key string into an ecdsa.SigningKey first to convert it to PEM.
        private_key_pem: bytes = ecdsa.SigningKey.from_string( #type: ignore
            string=bytearray.fromhex(self.private_key(index)),
            curve=SECP256k1,
            hashfunc=hashlib.sha256
        ).to_pem()

        # Ensuring that the public key string is in the payload
        if add_public_key:
            payload['public_key'] = self.public_key(index)

        # Creating and returning the JWT
        return jwt.encode( # type: ignore
            payload = payload,
            key = private_key_pem, # type: ignore
            algorithm = "ES256K"
        )