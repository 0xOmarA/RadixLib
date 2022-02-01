from radixlib.api_types.identifiers import AccountIdentifier
from radixlib.serializable import Serializable
from radixlib.api_types import TokenAmount
from typing import Dict, Any
import radixlib as radix
import json

class TransferTokens(Serializable):
    """ Defines a TransferTokens action  """

    def __init__(
        self,
        from_account: str,
        to_account: str,
        amount: int,
        token_rri: str,
    ) -> None:
        """ Instantiates a new TransferTokens action used for the creation of new tokens.

        Args:
            from_account (str): The account which will be sending the tokens.
            to_account (str): The account which will be getting the tokens.
            amount (int): The amount of tokens to send.
            token_rri (str): The RRI of the token to send.
        """

        self.from_account: AccountIdentifier = AccountIdentifier(from_account)
        self.to_account: AccountIdentifier = AccountIdentifier(to_account)
        self.amount: int = amount
        self.token_rri: str = token_rri

    def to_dict(self) -> Dict[str, Any]:
        """" Converts the object to a dictionary """
        return radix.utils.remove_none_values_recursively(
            radix.utils.convert_to_dict_recursively({
                "type": "TransferTokens",
                "from_account": self.from_account,
                "to_account": self.to_account,
                "amount": TokenAmount(
                    rri = self.token_rri,
                    amount = self.amount
                )
            })
        )

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(
        cls, 
        dictionary: Dict[Any, Any]
    ) -> 'TransferTokens':
        """ Loads a TransferTokens from a Gateway API response dictionary
        
        Args:
            dictionary (dict): The dictionary to load the object from

        Returns:
            TransferTokens: A new TransferTokens initalized from the dictionary
        
        Raises: 
            TypeError: Raised when the type of the action in the dictionary does not match
                the action name of the class
        """

        if dictionary.get('type') != "TransferTokens":
            raise TypeError(f"Expected a dictionary with a type of TransferTokens but got: {dictionary.get('type')}")

        return cls(
            from_account = dictionary['from_account']['address'],
            to_account = dictionary['to_account']['address'],
            amount = int(dictionary['amount']['value']),
            token_rri = dictionary['amount']['token_identifier']['rri']
        )

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'TransferTokens':
        """ Loads a TransferTokens from a Gateway API response JSON string. """
        return cls.from_dict(json.loads(json_string))