from radixlib.api_types.identifiers import AccountIdentifier, TokenIdentifier, ValidatorIdentifier
from radixlib.serializable import Serializable
from typing import Dict, Any
import radixlib as radix
import json

class StakeTokens(Serializable):
    """ Defines a StakeTokens action. """

    def __init__(
        self,
        from_account: str,
        to_validator: str,
        amount: int,
        token_rri: str,
    ) -> None:
        """ Instantiates a new StakeTokens action used for the creation of new tokens.

        Args:
            from_account (str): The account that is staking their tokens.
            to_validator (str): The validator to stake the tokens at.
            amount (int): The amount of tokens to send.
            token_rri (str): The RRI of XRD on that specific network

        Raises:
            ValueError: If the RRI given does not begin with XRD.
        """

        if not token_rri.lower().startswith('xrd'):
            raise ValueError("RRI provided is not of the network's native XRD token.")

        self.from_account: AccountIdentifier = AccountIdentifier(from_account)
        self.to_validator: ValidatorIdentifier = ValidatorIdentifier(to_validator)
        self.amount: int = amount
        self.token_rri: str = token_rri

    def to_dict(self) -> Dict[str, Any]:
        """" Converts the object to a dictionary """
        return radix.utils.remove_none_values_recursively(
            radix.utils.convert_to_dict_recursively({
                "type": "StakeTokens",
                "from_account": self.from_account,
                "to_validator": self.to_validator,
                "amount": {
                    "value": str(self.amount),
                    "token_identifier": TokenIdentifier(rri=self.token_rri)
                }
            })
        )

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(
        cls, 
        dictionary: Dict[Any, Any]
    ) -> 'StakeTokens':
        """ Loads a StakeTokens from a Gateway API response dictionary
        
        Args:
            dictionary (dict): The dictionary to load the object from

        Returns:
            StakeTokens: A new StakeTokens initalized from the dictionary
        
        Raises: 
            TypeError: Raised when the type of the action in the dictionary does not match
                the action name of the class
        """

        if dictionary.get('type') != "StakeTokens":
            raise TypeError(f"Expected a dictionary with a type of StakeTokens but got: {dictionary.get('type')}")

        return cls(
            from_account = dictionary['from_account']['address'],
            to_validator = dictionary['to_validator']['address'],
            amount = int(dictionary['amount']['value']),
            token_rri = dictionary['amount']['token_identifier']['rri']
        )

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'StakeTokens':
        """ Loads a StakeTokens from a Gateway API response JSON string. """
        return cls.from_dict(json.loads(json_string))