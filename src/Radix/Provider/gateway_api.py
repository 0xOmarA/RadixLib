from ..Types import NetworkType, StateIdentifier
from .. import utils
from typing import Optional, Union, Dict, List
import requests

class GatewayProvider():
    """ 
    A wrapper for the Gateway API which exposes the functions and endpoints in the gateway API in a 
    simple manner. 
    
    Link to offical Radix docs: https://docs.radixdlt.com/main/apis/gateway-api.html
    """

    # The default mainnet and stokenet addresses which are used by the Radix wallet.
    DEFAULT_MAINNET_ADDRESS: str = "https://mainnet.radixdlt.com"
    DEFAULT_STOKENET_ADDRESS: str = "https://stokenet.radixdlt.com"

    def __init__(
        self,
        network: NetworkType,
        custom_node_address: Optional[str] = None,
        open_api_version: str = "1.0.2"
    ) -> None:
        """
        Initializes a new gateway API using the network type provided and the optional custom node 
        address given. 

        # Arguments

        * `network: NetworkType` - The type of network to connect to.
        * `custom_node_address: Optional[str]` - An optional argument which defaults to None. You 
        may use this argument if you wish to connect to a custom node.
        * `open_api_version: str` - An string which describes the version of the open api used for 
        the gateway API. Defaults to `1.0.2`.
        """

        self.__open_api_version: str = open_api_version
        self.__network: NetworkType = network

        # Setting the base URL based on the passed parameters
        self.__base_url: str
        if custom_node_address:
            self.__base_url = custom_node_address
        else:
            self.__base_url = self.DEFAULT_MAINNET_ADDRESS if network.MAINNET else self.DEFAULT_STOKENET_ADDRESS

        # Stripping additional characters that might be at the end of the base url.
        self.__base_url = self.__base_url.strip('/\\') 
        
    @property
    def base_url(self) -> str:
        """ A getter method for the base url """
        return self.__base_url

    @property
    def open_api_version(self) -> str:
        """ A getter method for the open_api_version """
        return self.__open_api_version

    @property
    def network(self) -> NetworkType:
        """ A getter method for the network type """
        return self.__network

    def __str__(self) -> str:
        """ Represents the Provider as a string """
        return f'<GatewayProvider base_url="{self.base_url}">'

    def __repr__(self) -> str:
        """ Represents the Provider """
        return str(self)

    def __dispatch(
        self,
        endpoint: str,
        params: dict,
        http_method: Optional[str] = "POST"
    ) -> dict:
        """
        Dispatches an API call of the type `http_method` to the endpoint given with the data in the
        `params` argument.

        # Arguments

        * `endpoint: str` - A string of the endpoint which the call is being made to.
        * `params: dict` - A dictionary of the data to include in the request.
        * `http_method: str` - An optional string which defaults to POST. This argument describes 
        the type of the request to use for the API call.

        # Returns

        * `dict` - A dictionary of the response from the API.

        # Raises

        * `ValueError` - Raised if the `error` key is found in the response
        """

        # Adding the network_identifier to the parameters of the request
        params['network_identifier'] = {
            "network": str(self.network)
        }

        # Making the request using the passed arguments
        response: requests.Response = requests.request(
            method = str(http_method),
            url = f'{self.base_url}/{endpoint}',
            json = utils.remove_none_values_recursively(params),
            headers = {
                "X-Radixdlt-Target-Gw-Api": self.open_api_version
            }
        )
        response_json: dict = response.json()

        if 'error' in response_json.keys():
            raise ValueError(response_json)
        else:
            return response_json

    def get_gateway_info(self) -> dict:
        """ 
        Returns the Gateway API version, network and current ledger state.

        # Returns

        * `dict` - A dictionary of the API response
        """

        return self.__dispatch(
            endpoint = "gateway",
            params = {},
            http_method = "POST"
        )

    def derive_account_identifier(
        self,
        public_key: Union[str, bytes, bytearray]
    ) -> str:
        """
        Derives the account address from the public key. 

        # Arguments

        * `public_key: Union[str, bytes, bytearray]` - The public key used to derive the wallet 
        address from. Can be passed as a string, bytes, or a bytearray.

        # Returns

        * `str` - A string of the derived wallet address
        """

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
        )['account_identifier']['address']

    def get_account_balances(
        self,
        wallet_address: str,
        at_state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Dict[str, int]]:
        """
        Used to get the balance of the `wallet_address` at the specified state.

        # Arguments

        * `wallet_address: str` - A string of the wallet address to get the balances for.
        * `at_state_identifier: Optional[StateIdentifier]` - An optional state identifier which 
        allows a client to request a response referencing an earlier ledger state.

        # Returns

        * `dict` - A dictionary of the balances of the account in the following format
        
        ```json
        {
            "total_balance": {
                "rri1": 13030333302922222,
                "rri2": 13030333302922222
            },
            "staking_balance": {
                "xrd_rri": 13030333302922222
            },
            "liquid_balance": {
                "rri1": 13030333302922222,
                "rri2": 13030333302922222
            }
        }
        ```
        """

        # Getting the balances from the blockchain
        state_itentifier: dict = at_state_identifier.to_dict() if at_state_identifier is not None else {}
        balances: dict = self.__dispatch(
            endpoint = "account/balances",
            params = {
                "account_identifier": {
                    "address": wallet_address
                },
                "at_state_identifier": state_itentifier
            }
        )

        # Processing the balances into an easy to query dictionary format
        final_balances: Dict[str, Dict[str, int]] = {
            "total_balance": {},
            "staking_balance": {},
            "liquid_balance": {},
        }

        final_balances['staking_balance'][balances['account_balances']['staked_and_unstaking_balance']['token_identifier']['rri']] = int(balances['account_balances']['staked_and_unstaking_balance']['value'])
        for token_balance in balances['account_balances']['liquid_balances']:
            final_balances['liquid_balance'][token_balance['token_identifier']['rri']] = int(token_balance['value'])

        unique_rris: List[str] = list(set(list(final_balances['staking_balance'].keys()) + list(final_balances['liquid_balance'].keys())))
        
        for rri in unique_rris:
            balance1: int = final_balances['staking_balance'].get(rri)           
            balance2: int = final_balances['liquid_balance'].get(rri)     
            final_balances['total_balance'][rri] = (0 if balance1 is None else balance1) + (0 if balance2 is None else balance2)

        return final_balances

    def get_stake_positions(
        self,
        wallet_address: str,
        at_state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Dict[str, int]]:
        """
        Returns the xrd which the account has in pending and active delegated stake positions with 
        validators, given an account address. If an account address is valid, but doesn't have any 
        ledger transactions against it, this endpoint still returns a successful response

        # Arguments

        * `wallet_address: str` - A string of the wallet address to get the staking positions for.
        * `at_state_identifier: Optional[StateIdentifier]` - An optional state identifier which 
        allows a client to request a response referencing an earlier ledger state.

        # Returns

        * `dict` - A dictionary of the balances of the account in the following format
        
        ```json
        {
            "pending_stakes": [
                {
                    "validator_address": "address",
                    "amount": {
                        "xrd_rri": 123312123331233
                    },
                }
            ],
            "stakes": [
                {
                    "validator_address": "address",
                    "amount": {
                        "xrd_rri": 123312123331233
                    },
                }
            ]
        }
        ```
        """

        # Getting the stakes from the blockchain
        state_itentifier: dict = at_state_identifier.to_dict() if at_state_identifier is not None else {}
        stakes: dict = self.__dispatch(
            endpoint = "account/stakes",
            params = {
                "account_identifier": {
                    "address": wallet_address
                },
                "at_state_identifier": state_itentifier
            }
        )

        return {
            key: list(map(lambda x: dict([
                ('validator_address', x['validator_identifier']['address']),
                ('amount', {
                    x['delegated_stake']['token_identifier']['rri']: int(x['delegated_stake']['value'])
                })
            ]), value))
            for key, value 
            in stakes.items()
            if key in ['pending_stakes', 'stakes']
        }

    def get_unstake_positions(
        self,
        wallet_address: str,
        at_state_identifier: Optional[StateIdentifier] = None
    ) -> Dict[str, Dict[str, int]]:
        """
        Returns the xrd which the account has in pending and temporarily-locked delegated unstake 
        positions with validators, given an account address. If an account address is valid, but 
        doesn't have any ledger transactions against it, this endpoint still returns a successful 
        response.

        # Arguments

        * `wallet_address: str` - A string of the wallet address to get the staking positions for.
        * `at_state_identifier: Optional[StateIdentifier]` - An optional state identifier which 
        allows a client to request a response referencing an earlier ledger state.

        # Returns

        * `dict` - A dictionary of the balances of the account in the following format
        
        ```json
        {
            "pending_unstakes": [
                {
                    "validator_address": "address",
                    "amount": {
                        "xrd_rri": 123312123331233
                    },
                    "epochs_until_unlocked": 1290
                }
            ],
            "unstakes": [
                {
                    "validator_address": "address",
                    "amount": {
                        "xrd_rri": 123312123331233
                    },
                    "epochs_until_unlocked": 1290
                }
            ]
        }
        ```
        """

        # Getting the unstakes from the blockchain
        state_itentifier: dict = at_state_identifier.to_dict() if at_state_identifier is not None else {}
        unstakes: dict = self.__dispatch(
            endpoint = "account/unstakes",
            params = {
                "account_identifier": {
                    "address": wallet_address
                },
                "at_state_identifier": state_itentifier
            }
        )

        return {
            key: list(map(lambda x: dict([
                ('validator_address', x['validator_identifier']['address']),
                ('amount', {
                    x['delegated_stake']['token_identifier']['rri']: int(x['delegated_stake']['value'])
                }),
                ('epochs_until_unlocked', x['epochs_until_unlocked']),
            ]), value))
            for key, value 
            in unstakes.items()
            if key in ['pending_unstakes', 'unstakes']
        }