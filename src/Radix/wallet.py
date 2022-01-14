from typing import Dict, Optional, List, Union
from .transaction import Transaction
from .provider import Provider
from .network import Network
from .signer import Signer
from .action import Action
from .token import Token
from . import utils
import requests
import json
import re


class Wallet():
    """ 
    A class which connects a provider with a wallet and allows for transactions to be
    made using this given wallet through the supplied provider.

    The whole concept and idea behind this wallet object is that I would like for it to
    be more abstract and higher level than the basic provider implementation.
    """

    def __init__(
        self,
        provider: Provider,
        signer: Signer,
        index: int = 0
    ) -> None:
        """ 
        Instatiates a new Radix object through the provider and the signer objects passed
        to the object.

        # Arguments

        * `provider: Provider` - A provider object which connects to the Radix blockchain RPC
        API.
        * `signer: Signer` - A signer object which stores the public and private keys for the 
        given radix wallet.
        """

        self.__provider: Provider = provider
        self.__signer: Signer = signer
        self.__index: int = index
    
    @property
    def provider(self) -> Provider:
        """ A getter method for the Raidx provider. """
        return self.__provider

    @property
    def signer(self) -> Signer:
        """ A getter method for the Radix signer """
        return self.__signer

    @property
    def index(self) -> int:
        """ A getter method for the given index """
        return self.__index

    @property
    def wallet_address(self) -> str:
        """ A getter method for the wallet address """
        return self.signer.wallet_address(
            index = self.index,
            mainnet = True if self.provider.network is Network.MAINNET else False
        )

    @property
    def public_key(self) -> str:
        """ A getter method for the signer's public key """
        return self.signer.public_key(index = self.index)

    @property
    def private_key(self) -> str:
        """ A getter method for the signer's private key """
        return self.signer.private_key(index = self.index)

    def build_sign_and_send_transaction(
        self,
        actions: Union[Action, List[Action]],
        message: Optional[str] = None,
        encrypt_message: bool = False,
        encrypt_for_address: Optional[str] = None
    ) -> str:
        """
        A method which is used to build, sign, and then eventually send a transaction
        off to the blockchain. This method is used as a quick and higher level way to 
        make transactions.

        # Arguments

        * `actions: Union[Action, List[Action]]` - A list of the `Radix.Action` objects which we want to incldue in
        the transaction
        * `message: Optional[str]` - A message to include in the transaction.
        * `encrypt_message: bool` - A boolean which defines if the message included in the transaction should be 
        encrypted or not. The encryption used makes it so that only the wallet of the receiver can decode.
        * `encrypt_for_address: Optional[str]` - The address to encrypt the messages for. If this address is not provided,
        then it is assumed that you wish to encrypt the message for the first `to_address` in the actions

        # Returns

        * `str` - A string of the transaction hash for this transaction.

        # Raises

        * `KeyError` - A key error if any error is faced during the building, signing, or the sending of the 
        transaction.

        # Note

        When asking this function to encrypt the message, it will use the `to_address` in the first action where
        a `to_address is provided`.
        """

        encoded_message: str = None
        if message:
            # Encrypting the message if we need to encrypt it 
            if encrypt_message is True:
                # Converting the actions to a list if it's not already that
                actions: List[Action] = actions if isinstance(actions, list) else [actions]
                
                # Getting the address to use for the encypted message.
                addresses: List[str] = [action.to_dict()['to'] for action in actions if action.to_dict().get('to') is not None]

                encoded_message: str = utils.encrypt_message(
                    sender_private_key = self.private_key,
                    receiver_public_key = utils.wallet_address_to_public_key(addresses[0] if encrypt_for_address is None else encrypt_for_address),
                    message = message
                )
            else:
                encoded_message: str = "0000" + message.encode().hex()

        # Building the transaction through the data passed to the function
        response: dict = self.provider.build_transaction(
            actions = actions,
            fee_payer = self.wallet_address,
            message = encoded_message,
        ).json()

        if 'error' in response.keys():
            raise KeyError(f"An error was encountered while building the transaction. Error: {response}")

        # Signing the transaction information
        blob: str = response['result']['transaction']['blob']
        hash_of_blob_to_sign: str = response['result']['transaction']['hashOfBlobToSign']
        signed_data: str = self.signer.sign(hash_of_blob_to_sign, index = self.index)

        # Finalizing the transaction and sending it
        response: requests.Response = self.provider.finalize_transaction(
            blob = blob,
            signature_der = signed_data,
            public_key_of_signer = self.signer.public_key(index = self.index),
            immediateSubmit = True
        ).json()

        if 'error' in response.keys():
            raise KeyError(f"An error has occured when finalizing the transaction: {response['error']}")

        try:
            return response['result']['txID']
        except:
            return response['result']['transaction']['txID']

    def get_balances(self) -> Dict[str, int]:
        """ 
        This method queries the blockchain for the balances of the tokens that this person
        holds and returns a dictionary mapping of the token RRI and the balance of this token.

        # Returns

        * `Dict[str, int]` - A dictionary mapping which maps the RRI to the balance of the tokens
        """

        response: dict = self.provider.get_balances(
            address = self.signer.wallet_address(
                index = self.index,
                mainnet = True if self.provider.network is Network.MAINNET else False
            )
        ).json()

        if 'error' in response.keys():
            raise KeyError(f"Encountered an error when trying to get the balances: {response}")

        return {
            token_info['rri']: int(token_info['amount'])
            for token_info in response['result']['tokenBalances']
        }

    def get_balance_of_token(
        self,
        token: Union[str, Token]
    ) -> int:
        """
        Gets the balance for the specific token with the provided RRI.

        # Arguments

        * `token: Union[str, Token]` - Either a string of the token's RRI or a token object from
        which the RRI is obtained

        # Returns

        * `int` - An integer of the current balance for the provided token
        """

        # Getting the RRI from the token object if the `token` arg is a `Token`
        rri: str = token.rri if isinstance(token, Token) else token
        balance: int = self.get_balances().get(rri)
        
        return 0 if balance is None else balance

    def get_transaction_history(
        self,
        size: int,
    ) -> List[Transaction]:
        """
        A method used to get the transaction history for the loaded wallet.

        # Arguments

        * `size: int` - An optional integer value used to define the size or the maximum 
        number of transactions to retrieve from the API.

        # Returns

        * `List[Transaction]` - A sorted list of `Transaction` objects where item 0 is the 
        oldest transaction while item -1 is the newest transaction
        """
        # Getting the transactions for the wallet address
        response: dict = self.provider.get_transaction_history(
            address = self.wallet_address,
            size = size
        ).json()

        if 'error' in response.keys():
            raise KeyError(f"An error was encountered while getting the transaction history. Error: {response}")

        return sorted(list(map(lambda x: Transaction(**x), [{key.replace('txID', 'tx_id').replace('sentAt', 'sent_at'): value for key,value in transaction_info.items()} for transaction_info in response['result']['transactions']])), key = lambda x: x.sent_at)

    def get_transaction(
        self,
        tx_id: str
    ) -> Transaction:
        """
        Loads in a transaction object from the transaction id passed as an argument

        # Argument

        * `tx_id: str` - A string of the transaction id.

        # Returns

        * `Transaction` - A transaction object loaded from the transaction id
        """

        response: dict = self.provider.lookup_transaction(
            txID = tx_id
        ).json()

        if 'error' in response.keys():
            raise KeyError(f"An error was encountered while getting the transaction history. Error: {response}")

        return Transaction(**{key.replace('txID', 'tx_id').replace('sentAt', 'sent_at'): value for key,value in response['result'].items()})

    def get_token(
        self,
        rri: str
    ) -> Token:
        """
        A method used to get all of the token information from the Token's RRI.

        # Arguments

        * `rri: str` - A string of the Radix Resource Identifier (RRI) underwhich the
        token was created

        # Returns

        `Token` - A token object loaded with the token's information
        """

        response: dict = self.provider.get_token_info(
            rri = rri
        ).json()

        if 'error' in response.keys():
            raise KeyError(f"An error was encountered while getting the transaction history. Error: {response}")

        return Token(**{key.replace('tokenInfoURL', 'token_info_url').replace('currentSupply', 'current_supply').replace('iconURL', 'icon_url'): value for key, value in response['result'].items()})