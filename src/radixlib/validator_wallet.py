

from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from ecdsa.util import sigencode_der
import ecdsa
import hashlib

from radixlib.api_types.identifiers import AccountIdentifier, StateIdentifier
from radixlib.parsers import DefaultParser, ParserBase
from radixlib.actions import ActionType
from radixlib.network import Network
from radixlib import ActionBuilder
from radixlib import Provider
from radixlib.wallet import Wallet
import radixlib as radix
from typing import List, Union, Optional, Dict, Any, Tuple, Type

class ValidatorWallet(Wallet):
    """ Uses validator's keystore file and provider objects to create a higher level of abstraction and provide wallet
    functionality.
    """

    def __init__(
        self,
        provider: Provider,
        ecdsa_private_key: ecdsa.SigningKey
    ) -> None:
        """ Instantiates a new wallet object from the provider and signer given.

        Args:
            provider (Provider): The provider object used to provide connection to the gateway API.
            signer (Signer): The signer holding the public and private keys for the account.
            index (int): An integer which defaults to 0 and controls the account index used by the 
                wallet
        """

        self.provider: Provider = provider
        self.network: Network = provider.network
        self._ecdsa_private_key: ecdsa.SigningKey = ecdsa_private_key
        self.__parser: Type[ParserBase] = DefaultParser

    @property
    def public_key(self) -> str:
        """ A getter method for the public key """
        return radix.derive.public_key_from_ecdsa_private_key(self._ecdsa_private_key)

    @property
    def private_key(self) -> str:
        """ A getter method for the private key """
        return self._ecdsa_private_key.to_string()

    @property
    def validator_address(self) -> str:
        """
        a getter method for the validator_address
        """
        return radix.derive.validator_address_from_public_key(self.public_key, self.network)
    
    @classmethod
    def from_validator_keystore(
        clz, 
        provider: Provider, 
        filename: str, 
        password: str) -> 'ValidatorWallet':
        with open(filename, 'rb') as f:
            private_key, certificate, additional_certificated = pkcs12.load_key_and_certificates(f.read(),
            str.encode(password), default_backend())
        
        # Extract the unencrypted Private Key bytes
        private_key_bytes = private_key.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption())

        # Convert into Elliptic Curve Digital Signature Algorithm (ecdsa) private key object
        private_key = ecdsa.SigningKey.from_der(private_key_bytes, hashfunc=hashlib.sha256)
        return clz(provider, private_key)


    # ########################################
    # ---------- Quick Transactions ----------
    # ########################################

    def build_sign_and_send_transaction(
        self,
        actions: Union[List[ActionType], ActionBuilder],
        message_string: Optional[str] = None,
        encrypt_for_address: Optional[str] = None
    ) -> str:
        """ Provides a quick way of creating and sending transactions. This method is responsible
        for the creation, signing, and eventual submission of the transaction to the blockchain.
        
        Args:
            actions (Union[List[ActionType], radix.ActionBuilder]): Either a list of actions or an
                ActionBuilder used to build create the actions.
            message_string (str, optional): A string of the message to include in the transaction. 
                This stirng should be utf-8 encoded.
            encrypt_for_address (:obj:`str`, optional): An optional string of the address to encrypt
                the message for. If no address is given then 

        Returns:
            str: A string of the transaction hash

        Raises:
            KeyError: Raised if a problem occurs in the creation of the transaction and the key
                `transaction_build` can't be found in the object returned from the build process.
        """

        # Checking if a message was given or not. If a message has been given, then we perform the 
        # encryption if needed. 
        message_bytes: Optional[bytes]
        if message_string:
            encoded_message_hex: str
            if encrypt_for_address:
                encoded_message_hex = "01FF" + radix.utils.encrypt_message(
                    sender_private_key = self._ecdsa_private_key,
                    receiver_public_key = radix.derive.public_key_from_wallet_address(encrypt_for_address),
                    message = message_string
                )
            else:
                encoded_message_hex = "0000" + message_string.encode('utf-8').hex()

            message_bytes = bytearray.fromhex(encoded_message_hex)
        else:
            message_bytes = None

        # Building the transaction to get the transaction blob and the payload to sign.
        tx_info: Dict[Any, Any] = self.provider.build_transaction(
            actions = actions,
            fee_payer = self.address,
            message_bytes = message_bytes,
        )

        if 'transaction_build' not in tx_info.keys():
            raise KeyError(f"Transaction building failed: {tx_info}")

        # Submitting the transaction to the blockchain
        tx_submission_info: Dict[Any, Any] = self.provider.finalize_transaction(
            unsigned_transaction = tx_info['transaction_build']['unsigned_transaction'],
            # signature_der = self.signer.sign(tx_info['transaction_build']['payload_to_sign'], self.index),
            signature_der = self._ecdsa_private_key.sign_digest( #type: ignore
                digest = bytearray.fromhex(tx_info['transaction_build']['payload_to_sign']), 
                sigencode=sigencode_der
            ).hex(),
            public_key = self.public_key,
            submit = True,
        )

        print(tx_submission_info)
        return tx_submission_info['transaction_identifier']['hash']
