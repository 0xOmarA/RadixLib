from radixlib.serializable import Serializable
from typing import Dict
import json

class AccountIdentifier(Serializable):
    """ The implementation of an AccountIdentifier """

    def __init__(
        self,
        address: str
    ) -> None:
        """ Instantiates a new AccountIdentifier from the account's wallet address """

        self.address: str = address

    def __str__(self) -> str:
        """ Converts the object to a string """
        return f"""AccountIdentifier({", ".join(map(lambda x: "%s=%s" % x, self.to_dict().items()))})"""

    def __repr__(self) -> str:
        """ Represents an object """
        return str(self)

    def __eq__(self, other: 'object') -> bool:
        """ Checks for equality between self and other """
        return self.address == other.address if isinstance(other, AccountIdentifier) else False

    def to_dict(self) -> Dict[str, str]:
        """" Converts the object to a dictionary """
        return {
            "address": self.address
        }

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(
        cls,
        dictionary: Dict[str, str]
    ) -> 'AccountIdentifier':
        """ Creates a new instance of the AccountIdentifier from a dictionary

        This method is used to load up an AccountIdentifier from the dictionaries that are returned
        by the Gateway API.

        Args:
            dictionary (dict): A dictionary of the AccountIdentifier obtained from the Gateway API.

        Returns:
            AccountIdentifier: An AccountIdentifier loaded with the data
        """

        return cls(address = dictionary['address'])

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'AccountIdentifier':
        """ Creates a new instance of the AccountIdentifier from a string

        This method is used to load up an AccountIdentifier from the strings that are returned
        by the Gateway API.

        Args:
            json_string (str): The JSON serialzable strings returnd by the gateway API.

        Returns:
            AccountIdentifier: An AccountIdentifier loaded with the data
        """

        return cls.from_dict(json.loads(json_string))