from radixlib.api_types.identifiers import AccountIdentifier, ValidatorIdentifier
from radixlib.serializable import Serializable
from radixlib.api_types import TokenAmount
from typing import Dict, Any, Optional
import radixlib as radix
import json

class UnstakeTokens(Serializable):
    """ Defines an UnstakeTokens action  """

    def __init__(
        self,
        to_account: str,
        from_validator: str,
        unstake_percentage: Optional[float] = None,
        amount: Optional[int] = None,
        token_rri: Optional[str] = None,
    ) -> None:
        """ Instantiates a new UnstakeTokens action used for the creation of new tokens.

        Args:
            to_account (str): The account that is unstaking their tokens.
            from_validator (str): The validator to unstake the tokens from.
            amount (int, optional): The amount of tokens to send.
            token_rri (str, optional): The RRI of XRD on that specific network.
            unstake_percentage (float, optional): An optional argument of the percentage of tokens
                to unstake from the validator.

        Note:
            When calling this constructor, you need to specify one of the following:

                #. The amount and token rri together.
                #. The unstake percentage alone.

            One of the above two choices must be specified for a successful constructor call.

        Raises:
            ValueError: Raised in the following cases:

                #. When the token RRI given is not of the native XRD token.
                #. When the percentage amount given is not between 0 and 100.
        """

        # Checking if all of the arguments are none.
        if unstake_percentage is None and amount is None and token_rri is None:                 # None given
            raise ValueError("All of the amount specifiers were set to none. I can't tell how much you want to unstake.")
        elif unstake_percentage is not None and (amount is not None or token_rri is not None):  # All or some given
            raise ValueError("Conflict between the amount specifiers. You've specified the percentage to unstake and the amount to unstake. You can't specify both at the same time.")
        elif (amount is not None and token_rri is None) or (token_rri is None and amount is not None):
            raise ValueError("You did not specify a complete TokenAmount.")
        
        # Checking which of the aguments to set
        if unstake_percentage is not None:
            self.unstake_percentage: float = unstake_percentage
            if not (0 <= self.unstake_percentage <= 100):
                raise ValueError("The unstake percentage must be a number between 0 and 100.")
        elif amount is not None and token_rri is not None:
            self.amount: int = amount
            self.token_rri: str = token_rri

            if not token_rri.lower().startswith('xrd'):
                raise ValueError("RRI provided is not of the network's native XRD token.")

        self.to_account: AccountIdentifier = AccountIdentifier(to_account)
        self.from_validator: ValidatorIdentifier = ValidatorIdentifier(from_validator)

    def to_dict(self) -> Dict[str, Any]:
        """" Converts the object to a dictionary """
        return radix.utils.remove_none_values_recursively(
            radix.utils.convert_to_dict_recursively({
                "to_account": self.to_account,
                "from_validator": self.from_validator,
                "amount": TokenAmount(
                    rri = self.token_rri,
                    amount = self.amount
                ) if self.amount is not None else None,
                "unstake_percentage": self.unstake_percentage
            })
        )

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(
        cls, 
        dictionary: Dict[Any, Any]
    ) -> 'UnstakeTokens':
        """ Loads a UnstakeTokens from a Gateway API response dictionary
        
        Args:
            dictionary (dict): The dictionary to load the object from

        Returns:
            UnstakeTokens: A new UnstakeTokens initalized from the dictionary
        
        Raises: 
            TypeError: Raised when the type of the action in the dictionary does not match
                the action name of the class
        """

        if dictionary.get('type') != "UnstakeTokens":
            raise TypeError(f"Expected a dictionary with a type of UnstakeTokens but got: {dictionary.get('type')}")

        return cls(
            to_account = dictionary['to_account']['address'],
            from_validator = dictionary['from_validator']['address'],
            amount = None if dictionary.get('amount') is None else int(dictionary['amount']['value']),
            token_rri = None if dictionary.get('amount') is None else str(dictionary['amount']['token_identifier']['rri']),
            unstake_percentage = dictionary.get('unstake_percentage')
        )

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'UnstakeTokens':
        """ Loads a UnstakeTokens from a Gateway API response JSON string. """
        return cls.from_dict(json.loads(json_string))