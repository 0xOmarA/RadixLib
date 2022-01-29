from radixlib.identifiers import NetworkIdentifier, StateIdentifier, AccountIdentifier, TokenIdentifier, ValidatorIdentifier
from radixlib.exceptions.non_json_response import NonJsonResponseError
from radixlib.identifiers.transaction_identifier import TransactionIdentifier
from radixlib.actions import (
    CreateTokenDefinition,
)
from radixlib.network import Network
import radixlib as radix

from typing import Optional, Dict, Any, Union, List
import requests

class Provider():
    """ An implementation of a provider for the Gateway API of the Radix blockchain.
    
    This provider is implemented in a way that makes it easy to make requests to the API. However, 
    it is not the job of the provider to parse the responses from the API. The provider only goes 
    as far as trying to load in the response as json if its possible, but that is about it. This is 
    because the provider's job is to provide an easy way to communicate with the gateway API, not to
    parse responses.
    """

    # The default mainnet and stokenet addresses which are used by the Radix wallet.
    DEFAULT_MAINNET_ADDRESS: str = "https://mainnet.radixdlt.com"
    DEFAULT_STOKENET_ADDRESS: str = "https://stokenet.radixdlt.com"

    def __init__(
        self,
        network: Network,
        custom_gateway_url: Optional[str] = None,
        open_api_version: str = "1.0.3"
    ) -> None:
        """ Instantiates a new provider object through the passed parameters for the given network.
        
        This method is used to create a new provider object for the given network object passed in
        the arguments. The provider supports default RPC urls for both the mainnet and the stokenet.
        Aside from that, if you wish to connect to some other network, the :obj:`custom_gateway_url` 
        becomes nolonger an optional argument.

        Args:
            network (Network): The type of network that the provider will connect to.
            custom_gateway_url (:obj:`str`, optional): An optional argument that defaults to None. 
                This is the url of the RPC to connect to if we wish to connect to a custom gateway.
            open_api_version (str): An optional argument that defaults to "1.0.2" and it defines the
                value for the X-Radixdlt-Target-Gw-Api header which is requested by the gateway API.

        Raises:
            ValueError: Raised when a network other than the mainnet or the stokenet is used without
                providing a custom_gateway_url.
        """

        # Checking the network to see if we offer default gateway urls for these networks
        self.base_url: str
        if network == radix.network.MAINNET:
            self.base_url = self.DEFAULT_MAINNET_ADDRESS
        elif network == radix.network.STOKENET:
            self.base_url = self.DEFAULT_STOKENET_ADDRESS
        else:
            if custom_gateway_url is not None:
                self.base_url = custom_gateway_url
            else:
                raise ValueError(f"No default gateway url found for network for the network: {network.name}. You should either change the network or to supply a custom_gateway_url.")

        self.network: Network = network
        self.open_api_version: str = open_api_version

    def __str__(self) -> str:
        """ Represents the provider as a string """
        return f"Provider(base_url={self.base_url}, network={self.network.name}, open_api_version={self.open_api_version})"

    def __repr__(self) -> str:
        """ Represents the provider """
        return str(self)

    def __dispatch(
        self,
        endpoint: str,
        params: Dict[Any, Any],
        http_method: str = "POST"
    ) -> Dict[Any, Any]:
        """ Dispatches HTTP calls to the endpoints with the params provided

        Args:
            endpoint (str): The endpoint to make the HTTP call to.
            params (dict): The JSON payload to include in the request body.
            http_method (str): The type of request to make, defaults to a POST request.
        
        Returns:
            dict: A dictionary of the response from the API.
        """

        # The network identifier is always in the JSON body of all requests made to the dateway API.
        # So, we add the network identifier to the request parameters
        params['network_identifier'] = NetworkIdentifier(self.network)

        # Converting all of the parameter values to a dictionary if they inherit from the 
        # serializable class.
        dictionary_params: Dict[Any, Any] = radix.utils.convert_to_dict_recursively(params)

        # Making the request to the gateway API
        response: requests.Response = requests.request(
            method = str(http_method),
            url = f'{self.base_url}/{endpoint}',
            json = radix.utils.remove_none_values_recursively(dictionary_params),
            headers = {
                "X-Radixdlt-Target-Gw-Api": self.open_api_version
            }
        )

        # Checking the type of the content sent back from the API. If the content is in JSON then
        # we are good. If not then we throw an exception.
        if "application/json" not in response.headers['content-type']:
            raise NonJsonResponseError(
                f"The provider expects a JSON response but got a response of the type: "
                f"{response.headers['content-type']}. Response: {response.text}"
            )

        # Converting the response body to JSON and checking if there are errors in the response
        json_response: Dict[Any, Any] = response.json()

        return json_response

    # ---------- Gateway Endpoints ----------

    def get_gateway_info(self) -> Dict[str, Any]:
        """ Returns the Gateway API version, network and current ledger state. """

        return self.__dispatch(
            endpoint = "gateway",
            params = {}
        )

    # ---------- Account Endpoints ----------

    def derive_account_identifier(
        self,
        public_key: Union[str, bytes, bytearray]
    ) -> Dict[str, Any]:
        """ Derives the wallet address for the given public key.

        This method is similar to the `derive.wallet_address_from_public_key` method with the only 
        exception being that in this case we're asking the node to derive the accoutn identifier
        (wallet address) for us. This might be useful if a change suddenly happens to the network 
        and all of the HRPs are changed or any case where computing the wallet address locally does
        not make sense. 

        Args:
            public_key (Union[str, bytes, bytearray]): The public key to derive the wallet address 
                for.
        
        Returns:
            Dict[str, Any]: A dictionary of the account identifier.
        """

        # Casting the public key into an appropriate type
        pub_key: str
        if isinstance(public_key, (bytes, bytearray)):
            pub_key = public_key.hex()
        else:
            pub_key = public_key

        return self.__dispatch(
            endpoint = "account/derive",
            params = {
                "public_key": {
                    "hex": pub_key
                }
            }
        )

    def get_account_balances(
        self,
        account_identifier: AccountIdentifier,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Any]:
        """ Returns an account's available and staked token balances, given an account address. 
        
        Args:
            account_identifier (AccountIdentifier): The account to get the balances for.
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.
        
        Returns:
            dict: A dictionary of the account balances 
        """

        return self.__dispatch(
            endpoint = "account/balances",
            params = {
                "account_identifier": account_identifier,
                "at_state_identifier": state_identifier
            }
        )

    def get_stake_positions(
        self,
        account_identifier: AccountIdentifier,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Any]:
        """ Returns the xrd which the account has in pending and active delegated stake positions 
        with validators, given an account address.
        
        Args:
            account_identifier (AccountIdentifier): The account to get the stakes for.
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.
        
        Returns:
            dict: A dictionary of the account stake positions. 
        """

        return self.__dispatch(
            endpoint = "account/stakes",
            params = {
                "account_identifier": account_identifier,
                "at_state_identifier": state_identifier
            }
        )

    def get_unstake_positions(
        self,
        account_identifier: AccountIdentifier,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Any]:
        """ Returns the xrd which the account has in pending and temporarily-locked delegated 
        unstake positions with validators, given an account address.
        
        Args:
            account_identifier (AccountIdentifier): The account to get the unstakes for.
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.
        
        Returns:
            dict: A dictionary of the account unstake positions. 
        """

        return self.__dispatch(
            endpoint = "account/unstakes",
            params = {
                "account_identifier": account_identifier,
                "at_state_identifier": state_identifier
            }
        )

    def get_account_transactions(
        self,
        account_identifier: AccountIdentifier,
        state_identifier: Optional[StateIdentifier] = None,
        cursor: Optional[str] = None,
        limit: int = 30,
    ) -> Dict[str, Any]:
        """ Returns user-initiated transactions involving the given account address which have been
        succesfully committed to the ledger. The transactions are returned in a paginated format, 
        ordered by most recent.

        Args:
            account_identifier (AccountIdentifier): The account to get the transactions for.
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.
            cursor (:obj:`str`, optional): A timestamp of when to begin getting transactions.
            limit (int): The page size requested. The maximum value is 30 at present

        Returns:
            dict: A dictionary of the transactions information.
        """

        return self.__dispatch(
            endpoint = "account/transactions",
            params = {
                "account_identifier": account_identifier,
                "at_state_identifier": state_identifier,
                "cursor": cursor,
                "limit": limit
            },
        )

    # ---------- Token Endpoints ----------

    def get_native_token_info(
        self,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Any]:
        """ Returns information about XRD, including its Radix Resource Identifier (RRI).
        
        Args:
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary of the token information
        """

        return self.__dispatch(
            endpoint = "token/native",
            params = {
                "at_state_identifier": state_identifier,
            }
        )

    def get_token_info(
        self,
        token_identifier: TokenIdentifier,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Any]:
        """ Returns information about any token, given its Radix Resource Identifier (RRI).
        
        Args:
            token_identifier (TokenIdentifier): A token identifier for the token.
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary of the token information
        """

        return self.__dispatch(
            endpoint = "token",
            params = {
                "token_identifier": token_identifier,
                "at_state_identifier": state_identifier,
            }
        )

    def derive_token_identifier(
        self,
        public_key: Union[str, bytes, bytearray],
        symbol: str
    ) -> Dict[str, Any]:
        """ Returns the Radix Resource Identifier of a token with the given symbol, created by an 
        account with the given public key.
        
        Args:
            public_key (Union[str, bytes, bytearray]): The public key of the token creator.
            symbol (str): The 3 to 8 character long symbol assigned to the token.

        Returns:
            dict: A dictionary containing the token's RRI.
        """

        # Casting the public key into an appropriate type
        pub_key: str
        if isinstance(public_key, (bytes, bytearray)):
            pub_key = public_key.hex()
        else:
            pub_key = public_key

        return self.__dispatch(
            endpoint = "token/derive",
            params = {
                "symbol": symbol.lower(),
                "public_key": {
                    "hex": pub_key
                }
            }
        )

    # ---------- Validator Endpoints ----------

    def get_validator(
        self,
        validator_identifier: ValidatorIdentifier,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Any]:
        """ Returns information about a validator, given a validator address
        
        Args:
            validator_identifier (ValidatorIdentifier): An identifier for the validator to get info
                on.
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary of the validator info.
        """

        return self.__dispatch(
            endpoint = "validator",
            params = {
                "validator_identifier": validator_identifier,
                "at_state_identifier": state_identifier
            }
        )

    def get_validator_identifier(
        self,
        public_key: Union[str, bytes, bytearray],
    ) -> Dict[str, Any]:
        """ Returns the validator address associated with the given public key
        
        Args:
            public_key (Union[str, bytes, bytearray]): The public key of the validator

        Returns:
            dict: A dictionary of the validator info.
        """

        # Casting the public key into an appropriate type
        pub_key: str
        if isinstance(public_key, (bytes, bytearray)):
            pub_key = public_key.hex()
        else:
            pub_key = public_key

        return self.__dispatch(
            endpoint = "validator/derive",
            params = {
                "public_key": {
                    "hex": pub_key
                }
            }
        )

    def get_validators(
        self,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Any]:
        """ Returns information about all validators.
        
        Args:
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary of the validators
        """

        return self.__dispatch(
            endpoint = "validators",
            params = {
                "at_state_identifier": state_identifier
            }
        )

    # ---------- Transaction Endpoints ----------

    def get_transaction_rules(
        self,
        state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Any]:
        """ Returns the current rules used to build and validate transactions in the Radix Engine.

        Args:
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Returns:
            dict: A dictionary of the transaction rules.
        """

        return self.__dispatch(
            endpoint = "transaction/rules",
            params = {}
        )

    def build_transaction(
        self,
        actions: List[Union[CreateTokenDefinition, None]],
        fee_payer: AccountIdentifier,
        message_bytes: Optional[Union[str, bytes, bytearray]] = None,
        state_identifier: Optional[StateIdentifier] = None,
        disable_token_mint_and_burn: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """ Returns a built unsigned transaction payload, from a set of intended actions.
        
        Args:
            actions (:obj:`list` of :obj:`dict`): A list of action dictionaries.
            fee_payer (AccountIdentifier): An account identifier of the person paying the fees for 
                the transaction.
            message_bytes (Union[str, bytes, bytearray], optional): An optional argument for the 
                message to include in the transaction. This argument expects the bytes to be passed 
                to it. So, this should either be the hex string of the bytes or a bytes object.
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.
            disable_token_mint_and_burn (bool, optional): If true, mints and burns (aside from fee 
                payments) are not permitted during transaction execution.

        Returns:
            dict: A dictionary of the transaction details and blob
        """

        return self.__dispatch(
            endpoint = "transaction/build",
            params = {
                "at_state_identifier": state_identifier,
                "actions": list(map(lambda x: x.to_dict(), actions)),
                "fee_payer": fee_payer,
                "message": message_bytes.hex() if isinstance(message_bytes, (bytes, bytearray)) else message_bytes,
                "disable_token_mint_and_burn": disable_token_mint_and_burn
            }
        )

    def finalize_transaction(
        self,
        unsigned_transaction: Union[str, bytes, bytearray],
        signature_der: Union[str, bytes, bytearray],
        public_key: Union[str, bytes, bytearray],
        submit: Optional[bool] = None
    ) -> Dict[str, Any]:
        """ Returns a signed transaction payload and transaction identifier, from an unsigned 
        transaction payload and signature.
        
        Args:
            unsigned_transaction (Union[str, bytes, bytearray]): A bytes like object containing the
                transaction blob.
            signature_der (Union[str, bytes, bytearray]): A bytes like object of the signature in 
                the DER format.
            public_key (Union[str, bytes, bytearray]): A bytes like object of the public key of the
                signer.
            submit (Optional[bool]): An optional boolean which defines whether or not a transaction
                should be submitted immediately upon finalization.

        Returns:
            dict: A dictionary of the signed transaction information.
        """

        return self.__dispatch(
            endpoint = "transaction/finalize",
            params = {
                "unsigned_transaction": unsigned_transaction if isinstance(unsigned_transaction, str) else unsigned_transaction.hex(),
                "signature": {
                    "bytes": signature_der if isinstance(signature_der, str) else signature_der.hex(),
                    "public_key": {
                        "hex": public_key if isinstance(public_key, str) else public_key.hex(),
                    }
                },
                "submit": submit
            }
        )

    def submit_transaction(
        self,
        signed_transaction: Union[str, bytes, bytearray]
    ) -> Dict[str, Any]:
        """ Submits a signed transaction payload to the network. The transaction identifier from 
        finalize or submit can then be used to track the transaction status.
        
        Args:
            signed_transaction (Union[str, bytes, bytearray]): A string or bytes like object which 
                contains the bytes of the signed transaction to submit to the network.

        Returns:
            dict: A dictionary of the submitted transaction information.
        """

        return self.__dispatch(
            endpoint = "transaction/submit",
            params = {
                "signed_transaction": signed_transaction if isinstance(signed_transaction, str) else signed_transaction.hex(),
            }
        )

    def transaction_status(
        self,
        transaction_identifier: TransactionIdentifier,
        state_identifier: Optional[StateIdentifier] = None,
    ) -> Dict[str, Any]:
        """ Returns the status and contents of the transaction with the given transaction identifier.
        Transaction identifiers which aren't recognised as either belonging to a committed
        transaction or a transaction submitted through this Network Gateway may return a 
        TransactionNotFoundError. Transaction identifiers relating to failed transactions will, 
        after a delay, also be reported as a TransactionNotFoundError.
        
        Args:
            transaction_identifier (TransactionIdentifier): An identifier for the transaction
            state_identifier (:obj:`StateIdentifier`, optional): An optional argument that defaults 
                to None. Allows a client to request a response referencing an earlier ledger state.

        Return:
            dict: A dictionary of the transaction information.
        """

        return self.__dispatch(
            endpoint = "transaction/status",
            params = {
                "transaction_identifier": transaction_identifier,
                "at_state_identifier": state_identifier,
            }
        )