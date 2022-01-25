from ..Types import NetworkType
from typing import Optional, Union
import requests

class GatewayProvider():
    """ 
    A wrapper for the Gateway API which exposes the functions and endpoints in the 
    gateway API in a simple manner. 
    
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
            json = params,
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

        `str` - A string of the derived wallet address
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