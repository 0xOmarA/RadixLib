from radixlib.serializable import Serializable
from radixlib.network import Network
from typing import Dict, Union
import json

class NetworkIdentifier(Serializable):
    """ The implementation of an NetworkIdentifier """

    def __init__(
        self,
        network: Union[str, Network]
    ) -> None:
        """ Instantiates a new NetworkIdentifier from the network's name """

        self.network: str = network.name if isinstance(network, Network) else network

    def __str__(self) -> str:
        """ Converts the object to a string """
        return f"""NetworkIdentifier({", ".join(map(lambda x: "%s=%s" % x, self.to_dict().items()))})"""

    def __repr__(self) -> str:
        """ Represents an object """
        return str(self)

    def __eq__(self, other: 'object') -> bool:
        """ Checks for equality between self and other """
        return self.network == other.network if isinstance(other, NetworkIdentifier) else False

    def to_dict(self) -> Dict[str, str]:
        """" Converts the object to a dictionary """
        return {
            "network": self.network
        }

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(
        cls,
        dictionary: Dict[str, str]
    ) -> 'NetworkIdentifier':
        """ Creates a new instance of the NetworkIdentifier from a dictionary

        This method is used to load up an NetworkIdentifier from the dictionaries that are returned
        by the Gateway API.

        Args:
            dictionary (dict): A dictionary of the NetworkIdentifier obtained from the Gateway API.

        Returns:
            NetworkIdentifier: An NetworkIdentifier loaded with the data
        """

        return cls(network = dictionary['network'])

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'NetworkIdentifier':
        """ Creates a new instance of the NetworkIdentifier from a string

        This method is used to load up an NetworkIdentifier from the strings that are returned
        by the Gateway API.

        Args:
            json_string (str): The JSON serialzable strings returnd by the gateway API.

        Returns:
            NetworkIdentifier: An NetworkIdentifier loaded with the data
        """

        return cls.from_dict(json.loads(json_string))