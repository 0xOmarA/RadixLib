from radixlib.serializable import Serializable
from typing import Dict
import json

class TokenIdentifier(Serializable):
    """ The implementation of an TokenIdentifier """

    def __init__(
        self,
        rri: str
    ) -> None:
        """ Instantiates a new TokenIdentifier from the token's RRI. """

        self.rri: str = rri

    def __str__(self) -> str:
        """ Converts the object to a string """
        return f"""TokenIdentifier({", ".join(map(lambda x: "%s=%s" % x, self.to_dict().items()))})"""

    def __repr__(self) -> str:
        """ Represents an object """
        return str(self)

    def __eq__(self, other: 'object') -> bool:
        """ Checks for equality between self and other """
        return self.rri == other.rri if isinstance(other, TokenIdentifier) else False

    def to_dict(self) -> Dict[str, str]:
        """" Converts the object to a dictionary """
        return {
            "rri": self.rri
        }

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(
        cls,
        dictionary: Dict[str, str]
    ) -> 'TokenIdentifier':
        """ Creates a new instance of the TokenIdentifier from a dictionary

        This method is used to load up an TokenIdentifier from the dictionaries that are returned
        by the Gateway API.

        Args:
            dictionary (dict): A dictionary of the TokenIdentifier obtained from the Gateway API.

        Returns:
            TokenIdentifier: An TokenIdentifier loaded with the data
        """

        return cls(rri = dictionary['rri'])

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'TokenIdentifier':
        """ Creates a new instance of the TokenIdentifier from a string

        This method is used to load up an TokenIdentifier from the strings that are returned
        by the Gateway API.

        Args:
            json_string (str): The JSON serialzable strings returnd by the gateway API.

        Returns:
            TokenIdentifier: An TokenIdentifier loaded with the data
        """

        return cls.from_dict(json.loads(json_string))