from typing import Optional, Dict, Any
from radixlib.exceptions.non_json_response import NonJsonResponseError
from radixlib.identifiers import NetworkIdentifier
from radixlib.network import Network
import radixlib as radix
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
        open_api_version: str = "1.0.2"
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
        if response.headers['content-type'] != "application/json":
            raise NonJsonResponseError(
                f"The provider expectede a JSON response but got a response of the type: "
                f"{response.headers['content-type']}. Response: {response.text}"
            )

        # Converting the response body to JSON and checking if there are errors in the response
        json_response: Dict[Any, Any] = response.json()

        return json_response