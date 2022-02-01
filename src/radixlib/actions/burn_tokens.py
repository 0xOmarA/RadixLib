from radixlib.api_types.identifiers import AccountIdentifier
from radixlib.serializable import Serializable
from radixlib.api_types import TokenAmount
from typing import Dict, Any
import radixlib as radix
import json

class BurnTokens(Serializable):
    """ Defines a BurnTokens action  """

    def __init__(
        self,
        from_account: str,
        amount: int,
        token_rri: str,
    ) -> None:
        """ Instantiates a new BurnTokens action used for the creation of new tokens.

        Args:
            from_account (str): The account that the tokens will be burned from.
            amount (int, optional): The amount of tokens to mint.
            token_rri (str, optional): The RRI of the token.
        """

        self.from_account: AccountIdentifier = AccountIdentifier(from_account)
        self.amount: int = amount
        self.token_rri: str = token_rri

    def to_dict(self) -> Dict[str, Any]:
        """" Converts the object to a dictionary """
        return radix.utils.remove_none_values_recursively(
            radix.utils.convert_to_dict_recursively({
                "type": "BurnTokens",
                "from_account": self.from_account,
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
    ) -> 'BurnTokens':
        """ Loads a BurnTokens from a Gateway API response dictionary
        
        Args:
            dictionary (dict): The dictionary to load the object from

        Returns:
            BurnTokens: A new BurnTokens initalized from the dictionary
        
        Raises: 
            TypeError: Raised when the type of the action in the dictionary does not match
                the action name of the class
        """

        if dictionary.get('type') != "BurnTokens":
            raise TypeError(f"Expected a dictionary with a type of BurnTokens but got: {dictionary.get('type')}")

        return cls(
            from_account = dictionary['from_account']['address'],
            amount = int(dictionary['amount']['value']),
            token_rri = dictionary['amount']['token_identifier']['rri'],
        )

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'BurnTokens':
        """ Loads a BurnTokens from a Gateway API response JSON string. """
        return cls.from_dict(json.loads(json_string))