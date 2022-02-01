from radixlib.identifiers import AccountIdentifier, TokenIdentifier
from radixlib.serializable import Serializable
from typing import Dict, Any
import radixlib as radix
import json

class MintTokens(Serializable):
    """ Defines a MintTokens action  """

    def __init__(
        self,
        to_account: AccountIdentifier,
        amount: int,
        token_rri: str,
    ) -> None:
        """ Instantiates a new MintTokens action used for the creation of new tokens.

        Args:
            to_account (AccountIdentifier): The account that the tokens will be minted for.
            amount (int, optional): The amount of tokens to mint.
            token_rri (str, optional): The RRI of the token.
        """

        self.to_account: AccountIdentifier = to_account
        self.amount: int = amount
        self.token_rri: str = token_rri

    def to_dict(self) -> Dict[str, Any]:
        """" Converts the object to a dictionary """
        return radix.utils.remove_none_values_recursively(
            radix.utils.convert_to_dict_recursively({
                "to_account": self.to_account,
                "amount": {
                    "value": str(self.amount),
                    "token_identifier": TokenIdentifier(rri=self.token_rri).to_dict()
                },
                "type": "MintTokens"
            })
        )

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(
        cls, 
        dictionary: Dict[Any, Any]
    ) -> 'MintTokens':
        """ Loads a MintTokens from a Gateway API response dictionary
        
        Args:
            dictionary (dict): The dictionary to load the object from

        Returns:
            MintTokens: A new MintTokens initalized from the dictionary
        
        Raises: 
            TypeError: Raised when the type of the action in the dictionary does not match
                the action name of the class
        """

        if dictionary.get('type') != "MintTokens":
            raise TypeError(f"Expected a dictionary with a type of MintTokens but got: {dictionary.get('type')}")

        return cls(
            to_account = AccountIdentifier(dictionary['to_account']['address']),
            amount = dictionary['amount']['value'],
            token_rri = dictionary['amount']['token_identifier']['rri'],
        )

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'MintTokens':
        """ Loads a MintTokens from a Gateway API response JSON string. """
        return cls.from_dict(json.loads(json_string))