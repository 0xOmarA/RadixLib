from radixlib.api_types.identifiers import TokenIdentifier
from radixlib.serializable import Serializable
from typing import Dict, Any
import json

class TokenAmount(Serializable):
    """ The implementation of an TokenAmount """

    def __init__(
        self,
        rri: str,
        amount: int,
    ) -> None:
        """ Instantiates a new TokenAmount from the token's RRI. """

        self.rri: str = rri
        self.amount: int = amount

    def __str__(self) -> str:
        """ Converts the object to a string """
        return f"""TokenAmount({", ".join(map(lambda x: "%s=%s" % x, self.to_dict().items()))})"""

    def __repr__(self) -> str:
        """ Represents an object """
        return str(self)

    def __eq__(self, other: 'object') -> bool:
        """ Checks for equality between self and other """
        return self.rri == other.rri if isinstance(other, TokenAmount) else False

    def to_dict(self) -> Dict[str, Any]:
        """" Converts the object to a dictionary """
        return {
            "value": str(int(self.amount)),
            "token_identifier": TokenIdentifier(rri = self.rri).to_dict()
        }

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(
        cls,
        dictionary: Dict[str, Any]
    ) -> 'TokenAmount':
        """ Creates a new instance of the TokenAmount from a dictionary

        This method is used to load up an TokenAmount from the dictionaries that are returned
        by the Gateway API.

        Args:
            dictionary (dict): A dictionary of the TokenAmount obtained from the Gateway API.

        Returns:
            TokenAmount: An TokenAmount loaded with the data
        """

        return cls(
            amount = int(dictionary['value']),
            rri = TokenIdentifier.from_dict(dictionary['token_identifier']).rri
        )

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'TokenAmount':
        """ Creates a new instance of the TokenAmount from a string

        This method is used to load up an TokenAmount from the strings that are returned
        by the Gateway API.

        Args:
            json_string (str): The JSON serialzable strings returnd by the gateway API.

        Returns:
            TokenAmount: An TokenAmount loaded with the data
        """

        return cls.from_dict(json.loads(json_string))