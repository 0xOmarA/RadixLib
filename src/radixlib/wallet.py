from radixlib.api_types.identifiers import AccountIdentifier, StateIdentifier
from radixlib.parsers import DefaultParser, ParserBase
from radixlib.actions import ActionType
from radixlib.network import Network
from radixlib import ActionBuilder
from radixlib import Provider
from radixlib import Signer
import radixlib as radix
from typing import List, Union, Optional, Dict, Any, Tuple, Type

class Wallet():
    """ Uses signer and provider objects to create a higher level of abstraction and provide wallet
    functionaltiy.
    """

    def __init__(
        self,
        provider: Provider,
        signer: Signer,
        index: int = 0
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
        self.signer: Signer = signer
        self.index: int = index
        self.__parser: Type[ParserBase] = DefaultParser

    @property
    def public_key(self) -> str:
        """ A getter method for the public key """
        return self.signer.public_key(self.index)

    @property
    def private_key(self) -> str:
        """ A getter method for the private key """
        return self.signer.private_key(self.index)

    @property
    def address(self) -> str:
        """ A getter method for the wallet address """
        return radix.derive.wallet_address_from_public_key(
            public_key = self.public_key,
            network = self.network
        )

    @property
    def account_identifier(self) -> AccountIdentifier:
        """ Created an account identifier object from the wallet address """
        return AccountIdentifier(self.address)

    @property
    def action_builder(self) -> ActionBuilder:
        """ Creates a new action builder for the current network and returns it """
        return ActionBuilder(self.network)

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
                    sender_private_key = self.private_key,
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
            signature_der = self.signer.sign(tx_info['transaction_build']['payload_to_sign']),
            public_key = self.public_key,
            submit = True,
        )

        return tx_submission_info['transaction_identifier']['hash']

    # ###########################################
    # ---------- Query for Information ----------
    # ###########################################

    def get_account_balances(
        self,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Dict[str, int]]:
        """ Gets the account balance of the address and parses it through the 
        ``parse_account_balances`` parser.

        Args:
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary in the format described by the ``parse_account_balances`` parser.
        """
        
        return self.__parser.parse( # type: ignore
            data = self.provider.get_account_balances(self.address, state_identifier),
            data_type = 'get_account_balances'
        )

    def get_stake_positions(
        self,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """ Gets the stake positions of the currnetly loaded wallet and parses it through the 
        ``parse_stake_positions`` parser.
        
        Args:
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary in the format described by the ``parse_stake_positions`` parser.
        """

        return self.__parser.parse( # type: ignore
            data = self.provider.get_stake_positions(self.address, state_identifier),
            data_type = "get_stake_positions"
        )

    def get_unstake_positions(
        self,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """ Gets the unstake positions of the currnetly loaded wallet and parses it through the 
        ``parse_unstake_positions`` parser.
        
        Args:
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary in the format described by the ``parse_unstake_positions`` parser.
        """

        return self.__parser.parse( # type: ignore
            data = self.provider.get_unstake_positions(self.address, state_identifier),
            data_type = "get_unstake_positions"
        )

    def get_account_transactions(
        self,
        limit: int = 30,
        cursor: Optional[str] = None,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        """ Gets the transaction history for the currenty loaded wallet and parses it through the
        ``parse_account_transactions`` parser.

        Args:
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.
            cursor (:obj:`str`, optional): A timestamp of when to begin getting transactions.
            limit (int): The page size requested. The maximum value is 30 at present        

        Returns:
            tuple: A tuple fo an optional string which is of the next cursor and a list of dicts 
                which is of the parsed transactions
        """

        # The response of the API to the get transaction query
        api_response: Dict[str, Any] = self.provider.get_account_transactions(
            account_address = self.address,
            state_identifier = state_identifier,
            cursor = cursor,
            limit = limit
        )

        # Return the next cursor if it's given and the parsed transactions list
        return (
            api_response.get('next_cursor'),
            self.__parser.parse( # type: ignore
                data = api_response,
                data_type = "get_account_transactions"
            )
        )

    def get_native_token_info(
        self,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Any]:
        """ Gets the information of the native token of the network and parses it through the 
        ``parse_token_info`` parser.

        Args:
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary in the format described by the ``parse_token_info`` parser.
        """

        return self.__parser.parse( # type: ignore
            data = self.provider.get_native_token_info(state_identifier),
            data_type = "get_native_token_info"
        )

    def get_token_info(
        self,
        token_rri: str, 
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Any]:
        """ Gets the information of the native token of the network and parses it through the 
        ``parse_token_info`` parser.

        Args:
            token_rri (str): The RRI of the token to get the information for.
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary in the format described by the ``parse_token_info`` parser.
        """

        return self.__parser.parse( # type: ignore
            data = self.provider.get_token_info(token_rri, state_identifier),
            data_type = "get_token_info"
        )

    def derive_token_identifier(
        self,
        symbol: str
    ) -> str:
        """ Derives the RRI of a token created by this account.

        Args:
            symbol (str): The 3 to 8 character long symbol assigned to the token.

        Returns:
            str: A string of the derived token identifier.
        """

        return self.__parser.parse( # type: ignore
            data = self.provider.derive_token_identifier(self.public_key, symbol),
            data_type = "derive_token_identifier"
        )

    def get_validator(
        self,
        validator_address: str,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Any]:
        """ Gets the information for a given validator and parses it through the 
        ``parse_validator_info`` parser
        
        Args:
            validator_address (str): An identifier for the validator to get info on.
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary in the format described by the ``parse_validator_info`` parser.
        """

        return self.__parser.parse( # type: ignore
            data = self.provider.get_validator(validator_address, state_identifier),
            data_type = "get_validator"
        )


    def get_validators(
        self,
        state_identifier: Optional[StateIdentifier] = None
    ) -> List[Dict[str, Any]]:
        """ Gets the information of all of the validators on the network and parses it through the 
        ``parse_validator_info`` parser.
        
        Args:
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary in the format described by the ``parse_validator_info`` parser.
        """

        return self.__parser.parse( # type: ignore
            data = self.provider.get_validators(),
            data_type = "get_validators"
        )

    def transaction_status(
        self,
        transaction_hash: str,
        state_identifier: Optional[StateIdentifier] = None,
    ) -> Dict[str, Any]:
        """Returns the status and contents of the transaction with the given transaction identifier.
        Transaction identifiers which aren't recognised as either belonging to a committed
        transaction or a transaction submitted through this Network Gateway may return a 
        TransactionNotFoundError. Transaction identifiers relating to failed transactions will, 
        after a delay, also be reported as a TransactionNotFoundError.
        
        Args:
            transaction_hash (str): An identifier for the transaction
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary in the format described by the ``parse_validator_info`` parser.
        """

        return self.__parser.parse( # type: ignore
            data = self.provider.transaction_status(transaction_hash, state_identifier),
            data_type = "transaction_status"
        )