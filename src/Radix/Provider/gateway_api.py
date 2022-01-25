from ..Types import NetworkType
from typing import Optional
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
        open_api_version: Optional[str] = "1.0.2"
    ) -> None:
        """
        Initializes a new gateway API using the network type provided and the optional custom node 
        address given. 

        # Arguments

        * `network: NetworkType` - The type of network to connect to.
        * `custom_node_address: Optional[str]` - An optional argument which defaults to None. You 
        may use this argument if you wish to connect to a custom node.
        * `open_api_version: Optional[str]` - An optional string which describes the version of the
        open api used for the gateway API.
        """

        self.__open_api_version: str = open_api_version

        # Setting the base URL based on the passed parameters
        self.__base_url: str
        if custom_node_address:
            self.__base_url = custom_node_address
        else:
            self.__base_url = self.DEFAULT_MAINNET_ADDRESS if network.MAINNET else self.DEFAULT_STOKENET_ADDRESS

        # Stripping additional characters that might be at the end of the base url.
        self.__base_url = self.__base_url.strip('/\\') 