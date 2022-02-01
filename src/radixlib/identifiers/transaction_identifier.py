from radixlib.serializable import Serializable
from typing import Dict
import json

class TransactionIdentifier(Serializable):
    """ The implementation of an TransactionIdentifier """

    def __init__(
        self,
        hash: str
    ) -> None:
        """ Instantiates a new TransactionIdentifier from the transaction's hash. """

        self.hash: str = hash

    def __str__(self) -> str:
        """ Converts the object to a string """
        return f"""TransactionIdentifier({", ".join(map(lambda x: "%s=%s" % x, self.to_dict().items()))})"""

    def __repr__(self) -> str:
        """ Represents an object """
        return str(self)

    def __eq__(self, other: 'object') -> bool:
        """ Checks for equality between self and other """
        return self.hash == other.hash if isinstance(other, TransactionIdentifier) else False

    def to_dict(self) -> Dict[str, str]:
        """" Converts the object to a dictionary """
        return {
            "hash": self.hash
        }

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(
        cls,
        dictionary: Dict[str, str]
    ) -> 'TransactionIdentifier':
        """ Creates a new instance of the TransactionIdentifier from a dictionary

        This method is used to load up an TransactionIdentifier from the dictionaries that are returned
        by the Gateway API.

        Args:
            dictionary (dict): A dictionary of the TransactionIdentifier obtained from the Gateway API.

        Returns:
            TransactionIdentifier: An TransactionIdentifier loaded with the data
        """

        return cls(hash = dictionary['hash'])

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'TransactionIdentifier':
        """ Creates a new instance of the TransactionIdentifier from a string

        This method is used to load up an TransactionIdentifier from the strings that are returned
        by the Gateway API.

        Args:
            json_string (str): The JSON serialzable strings returnd by the gateway API.

        Returns:
            TransactionIdentifier: An TransactionIdentifier loaded with the data
        """

        return cls.from_dict(json.loads(json_string))