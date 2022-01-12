from typing import Optional, List, Dict, Tuple, Union
from .network import Network
from .action import Action
import requests
import re


class Provider():
    """ A wrapper for the Radix API. Created as per the documentation at: https://documenter.getpostman.com/view/14449947/TzscoSDW """

    # The default mainnet and stokenet addresses which are used by the Radix wallet.
    DEFAULT_MAINNET_ADDRESS: str = "https://mainnet.radixdlt.com"
    DEFAULT_STOKENET_ADDRESS: str = "https://stokenet.radixdlt.com"

    def __init__(
        self,
        network: Network,
        custom_node_address: Optional[str] = None,
        jsonrpc: str = "2.0"
    ) -> None:
        """
        Instantiates a new API instance using either the network parameter passed or the custom
        node address given as an argument.

        # Arguments

        * `network: Network` - A network argument of an enum of the type `Raidx.Network` used to 
        define the type of network to connect to.
        * `custom_node_address: Optional[str]` - An optional node address which you would like
        the API object to use in the queries.
        * `jsonrpc: str` - The string of the version of the JSONRPC to use. Defaults to 2.0.

        # Raises

        * `InvalidURL` - If an invalid url is given in the `custom_node_address` parameter.

        # Note

        When creating a new `API` object, you need to provide either the `network` parameter or
        the `custom_node_address` parameter. You can not provide both at the same time.
        """

        self.jsonrpc: str = jsonrpc
        self.network: Network = network
        
        # If a custom node address was provided, then check to make sure that
        # it is a valid url which uses the HTTP or HTTPS protocol
        url_regex: re.Pattern = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
        if custom_node_address is not None and not url_regex.match(custom_node_address):
            raise requests.exceptions.InvalidURL(f"The provided url: '{custom_node_address}' is not a valid url.")

        # Setting base url of the API object depending on the passed params
        self.base_url: str
        if custom_node_address is not None:
            self.base_url = custom_node_address.strip('\\').strip('//')
        else:
            self.base_url = self.DEFAULT_MAINNET_ADDRESS if network is Network.MAINNET else self.DEFAULT_STOKENET_ADDRESS

    def __dispatch(
        self,
        endpoint: str,
        http_method: str,
        api_method: str,
        params: dict,
        id: int,
        username_password: Optional[Tuple[str, str]] = None
    ) -> requests.Response:
        """
        The dispatcher method used to dispatch the API calls to the correct endpoint with the correct
        data.

        # Arguments

        * `endpoint: str` - A string of the name of the endpoint to make the API call to
        * `http_method: str` - A string of the HTTP method to use for the API call. Example: `POST`, `GET`.
        * `api_methpd: str` - A string of the API method to use. Example: `tokens.get_native_token`.
        * `params: dict` - A dictionary of the parameters for the API query.
        * `id: int` - An integer of the ID to use.
        * `username_password: Optional[Tuple[str, str]]` - Some of the API endpoints in Radix require a
        username and a password for the Basic HTTP Auth. The username and password required may be given 
        through this argument here.

        # Returns

        * `dict` - A dictionary of the response of the API to the query.
        """

        return requests.request(
            method=http_method,
            url=f"{self.base_url}/{endpoint}",
            json={
                "jsonrpc": self.jsonrpc,
                "method": api_method,
                "params": {key: value for key, value in params.items() if value is not None},
                "id": id
            },
            auth=username_password
        )

    def get_native_token(self) -> requests.Response:
        """
        Returns information about the native token of the network.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="tokens.get_native_token",
            params={},
            id=1,
        )

    def get_token_info(
        self,
        rri: str,
    ) -> requests.Response:
        """
        Return token information on the provided RRI.

        # Arguments
        * `rri: str` - The Radix Resource Identifier (RRI) which we wish to 
        get the token information for.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="tokens.get_info",
            params={
                "rri": rri,
            },
            id=1,
        )

    def get_balances(
        self,
        address: str,
    ) -> requests.Response:
        """
        Get the token balances for an address.

        # Arguments
        * `address: str` - The address which we wish to find the balance of.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="account.get_balances",
            params={
                "address": address,
            },
            id=1,
        )

    def get_transaction_history(
        self,
        address: str,
        size: int,
        cursor: Optional[str] = None,
        verbose: Optional[bool] = None,
    ) -> requests.Response:
        """
        Get the paginated transaction history for an address.

        # Arguments
        * `address: str` - The radix address which we wish to get the history for.
        * `size: int` - The size or number of transactions to get.
        * `cursor: Optional[str]` - The beginning of when we get the transactions.
        * `verbose: Optional[bool]` - Controls if the operation is verbose.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="account.get_transaction_history",
            params={
                "address": address,
                "size": size,
                "cursor": cursor,
                "verbose": verbose,
            },
            id=1,
        )

    def get_stake_positions(
        self,
        address: str,
    ) -> requests.Response:
        """
        Get stakes that have not been requested to be unstaked.

        # Arguments
        * `address: str` - The address which we wish to get the stake positions for.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="account.get_stake_positions",
            params={
                "address": address,
            },
            id=1,
        )

    def get_unstake_positions(
        self,
        address: str,
    ) -> requests.Response:
        """
        Get unstake history for an address.

        # Arguments
        * `address: str` - The address which we wish to get the unstake positions
        for.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="account.get_unstake_positions",
            params={
                "address": address,
            },
            id=1,
        )

    def lookup_transaction(
        self,
        txID: str,
    ) -> requests.Response:
        """
        Get a transaction from its txID.

        # Arguments
        * `txID: str` - The id or hash of the transactions which we wish to get
        the information for.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="transactions.lookup_transaction",
            params={
                "txID": txID,
            },
            id=1,
        )

    def get_transaction_status(
        self,
        txID: str,
    ) -> requests.Response:
        """
        Returns the status of a transaction.

        # Arguments
        * `txID: str` - The id or hash of the transactions which we wish to get
        the information for.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="transactions.get_transaction_status",
            params={
                "txID": txID,
            },
            id=1,
        )

    def get_next_epoch_set(
        self,
        size: int,
        cursor: Optional[str] = None,
    ) -> requests.Response:
        """
        Get a paginated validator list, ordered by XRD staked descending.

        # Arguments
        * `size: str` - The number of validators to retrieve.
        * `cursor: Optional[str]` - The cursor at which we begin the retrieval.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="validators.get_next_epoch_set",
            params={
                "size": size,
                "cursor": cursor,
            },
            id=1,
        )

    def lookup_validator(
        self,
        validator_address: str,
    ) -> requests.Response:
        """
        Lookup a single validator by its validator address.

        # Arguments
        * `validator_address: str` - The address of the validator which we wish
        to find the information on.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="validators.lookup_validator",
            params={
                "validatorAddress": validator_address,
            },
            id=1,
        )

    def get_id(self) -> requests.Response:
        """
        Get the network id, a number that uniquely identifies the network. 
        This network id must match the one used to derive addresses.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="network.get_id",
            params={},
            id=1,
        )

    def get_throughput(self) -> requests.Response:
        """
        Returns the average number of transaction per second committed to the ledger.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="network.get_throughput",
            params={},
            id=1,
        )

    def get_demand(self) -> requests.Response:
        """
        Average number of transactions submitted to the mempool per second.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="archive",
            http_method="POST",
            api_method="network.get_demand",
            params={},
            id=1,
        )

    def build_transaction(
        self,
        actions: Union[Action, List[Action]],
        fee_payer: str,
        message: Optional[str] = None,
        disableResourceAllocationAndDestroy: Optional[bool] = None,
    ) -> requests.Response:
        """
        Get an unsigned transaction.

        # Arguments
        
        * `actions: Union[Action, List[Action]]` - A list of the `Radix.Action` objects which we want to incldue in
        the transaction
        * `fee_payer: str` - A string of the address which will be paying the fees of the transaction.
        * `message: Optional[str]` - A message to include in the transaction.
        * `disableResourceAllocationAndDestroy: Optional[bool]` - A boolean which controls the allocation and 
        destruction of resources.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        if isinstance(actions, Action):
            actions: List[Action] = [actions]

        return self.__dispatch(
            endpoint="construction",
            http_method="POST",
            api_method="construction.build_transaction",
            params={
                "actions": list(map(Action.to_dict, actions)),
                "feePayer": fee_payer,
                "message": message,
                "disableResourceAllocationAndDestroy": disableResourceAllocationAndDestroy,
            },
            id=1,
        )

    def finalize_transaction(
        self,
        blob: str,
        signature_der: str,
        public_key_of_signer: str,
        immediateSubmit: Optional[bool] = True,
    ) -> requests.Response:
        """
        Finalizes a signed transaction before submitting it.

        # Arguments
        * `blob: str` - A string of the block of data to incldue the transaction.
        * `signature_der: str` - A string of the signed blob data.
        * `public_key_of_signer: str` - A string of the public key which the signer uses.
        * `immediateSubmit: Optional[bool]` - A boolean which defines if the transaction should be submitted
        immedietly.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="construction",
            http_method="POST",
            api_method="construction.finalize_transaction",
            params={
                "blob": blob,
                "signatureDER": signature_der,
                "publicKeyOfSigner": public_key_of_signer,
                "immediateSubmit": immediateSubmit,
            },
            id=0,
        )

    def submit_transaction(
        self,
        blob: str,
        txID: Optional[str] = None,
    ) -> requests.Response:
        """
        Submits a transaction to be dispatched to Radix network.

        # Arguments
        * `blob: str` - A string of the blob to include in the transaction.
        * `txID: Optional[str]` - An optional string of the transaction hash. This argument
        is usually used when we have called `finalize_transaction` with the `immediateSubmit`
        being `False`. In this case we get the `txID` from the `finalize_transaction` call 
        and then we submit it through this function.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="construction",
            http_method="POST",
            api_method="construction.submit_transaction",
            params={
                "blob": blob,
                "txID": txID,
            },
            id=0,
        )

    def get_account_info(self) -> requests.Response:
        """
        Your account's address and balances.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="account",
            http_method="POST",
            api_method="account.get_info",
            params={},
            id=1,
        )

    def submit_transaction_single_step(
        self,
        actions: List[Action],
        message: Optional[str] = None,
        disableResourceAllocationAndDestroy: Optional[bool] = None,
    ) -> requests.Response:
        """
        One step transaction submission. Resulting transaction is signed with nodes' private key

        # Arguments
        * `actions: List[Action]` - A list of the `Radix.Action` objects which we want to incldue in
        the transaction
        * `message: str` - A message to include in the transaction
        * `disableResourceAllocationAndDestroy: bool` - A boolean which controls the allocation and 
        destruction of resources.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="account",
            http_method="POST",
            api_method="account.submit_transaction_single_step",
            params={
                "actions": list(map(Action.to_dict, actions)),
                "message": message,
                "disableResourceAllocationAndDestroy": disableResourceAllocationAndDestroy,
            },
            id=1,
        )

    def get_api_configuration(self) -> requests.Response:
        """
        Get active configuration parameters for api

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="api.get_configuration",
            params={},
            id=1,
        )

    def get_api_data(self) -> requests.Response:
        """
        Get data for api

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="api.get_data",
            params={},
            id=1,
        )

    def get_consensus_configuration(self) -> requests.Response:
        """
        Get active configuration parameters for consensus

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="bft.get_configuration",
            params={},
            id=1,
        )

    def get_consensus_data(self) -> requests.Response:
        """
        Get data for consensus

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="bft.get_data",
            params={},
            id=1,
        )

    def get_mempool_configuration(self) -> requests.Response:
        """
        Get active configuration parameters for mempool

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="mempool.get_configuration",
            params={},
            id=1,
        )

    def get_mempool_data(self) -> requests.Response:
        """
        Get data for mempool

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="mempool.get_data",
            params={},
            id=1,
        )

    def get_latest_proof(self) -> requests.Response:
        """
        Get the latest known ledger proof

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="ledger.get_latest_proof",
            params={},
            id=1,
        )

    def get_latest_epoch_proof(self) -> requests.Response:
        """
        Get the latest known ledger epoch proof

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="ledger.get_latest_epoch_proof",
            params={},
            id=1,
        )

    def get_radix_engine_configuration(self) -> requests.Response:
        """
        Get active configuration parameters for radix engine

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="radix_engine.get_configuration",
            params={},
            id=1,
        )

    def get_radix_engine_data(self) -> requests.Response:
        """
        Get data for radix engine

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="radix_engine.get_data",
            params={},
            id=1,
        )

    def get_sync_configuration(self) -> requests.Response:
        """
        Get active configuration parameters for sync

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="sync.get_configuration",
            params={},
            id=1,
        )

    def get_sync_data(self) -> requests.Response:
        """
        Get data for sync

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="sync.get_data",
            params={},
            id=1,
        )

    def get_network_configuration(self) -> requests.Response:
        """
        Get active configuration parameters for networking

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="networking.get_configuration",
            params={},
            id=1,
        )

    def get_peers(self) -> requests.Response:
        """
        Get information about connected peer nodes

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="networking.get_peers",
            params={},
            id=1,
        )

    def get_address_book(self) -> requests.Response:
        """
        Get information about known peer nodes

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="networking.get_address_book",
            params={},
            id=1,
        )

    def get_networking_data(self) -> requests.Response:
        """
        Get data for networking

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="networking.get_data",
            params={},
            id=1,
        )

    def get_checkpoints(self) -> requests.Response:
        """
        Get genesis txn and proof,

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="checkpoints.get_checkpoints",
            params={},
            id=1,
        )

    def get_node_info(self) -> requests.Response:
        """
        Get information about node as a validator - stakes, registration status, etc.

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="validation.get_node_info",
            params={},
            id=1,
        )

    def get_current_epoch_data(self) -> requests.Response:
        """
        Get information about the current epoch's validator set

        # Returns

        * `requests.Response` - A response object of the response and other useful info such
        as the status code.
        """

        return self.__dispatch(
            endpoint="system",
            http_method="POST",
            api_method="validation.get_current_epoch_data",
            params={},
            id=1,
        )
